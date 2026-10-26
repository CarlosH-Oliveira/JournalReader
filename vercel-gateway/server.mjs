import http from 'node:http';
import { spawn } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { Readable } from 'node:stream';
import { get, put, del, list, issueSignedToken, presignUrl } from '@vercel/blob';

// SDK oficial em loopback: nenhuma rota administrativa fica exposta ao navegador.
const secret = randomBytes(32).toString('hex');
const json = (res, status, value) => { res.writeHead(status, { 'content-type': 'application/json' }); res.end(JSON.stringify(value)); };
const server = http.createServer(async (req, res) => {
  if (req.headers['x-internal-secret'] !== secret) return json(res, 403, { error: 'Forbidden' });
  const url = new URL(req.url, 'http://localhost');
  const path = url.searchParams.get('path');
  const auth = req.headers['x-vercel-oidc-token'] ? { oidcToken: req.headers['x-vercel-oidc-token'] } : {};
  try {
    if (url.pathname === '/sign' && req.method === 'POST') {
      if (!/^uploads\/[a-f0-9]{32}\/[a-f0-9]{32}\.(epub|pdf|txt)$/.test(path ?? '')) return json(res, 400, { error: 'Invalid path' });
      const validUntil = Date.now() + 15 * 60 * 1000;
      const constraints = { maximumSizeInBytes: 50 * 1024 * 1024, allowedContentTypes: ['application/octet-stream'] };
      const token = await issueSignedToken({ pathname: path, operations: ['put'], validUntil, ...constraints, ...auth });
      const result = await presignUrl(token, { operation: 'put', pathname: path, access: 'private', validUntil,
        ...constraints, addRandomSuffix: false, allowOverwrite: false });
      return json(res, 200, result);
    }
    if (url.pathname === '/keys' && req.method === 'GET') {
      const keys = []; let cursor;
      do {
        const page = await list({ prefix: 'keys/', cursor, ...auth });
        for (const blob of page.blobs) {
          const result = await get(blob.pathname, { access: 'private', useCache: false, ...auth });
          if (result?.statusCode === 200) keys.push(await new Response(result.stream).text());
        }
        cursor = page.hasMore ? page.cursor : undefined;
      } while (cursor);
      return json(res, 200, keys);
    }
    if (url.pathname !== '/object' || !path || !/^(uploads|state|drafts|keys)\/[a-zA-Z0-9/_.-]+$/.test(path) || path.includes('..')) return json(res, 400, { error: 'Invalid path' });
    if (req.method === 'GET') {
      const result = await get(path, { access: 'private', useCache: false, ...auth });
      if (!result) return json(res, 404, { error: 'Not found' });
      if (result.statusCode !== 200) return json(res, result.statusCode, { error: 'Read failed' });
      res.writeHead(200, { 'content-type': 'application/octet-stream', 'etag': result.blob.etag, 'content-length': result.blob.size });
      Readable.fromWeb(result.stream).pipe(res); return;
    }
    if (req.method === 'PUT') {
      const etag = req.headers['if-match'];
      const blob = await put(path, Readable.toWeb(req), { access: 'private', addRandomSuffix: false,
        allowOverwrite: Boolean(etag), ...(etag ? { ifMatch: etag } : {}), contentType: 'application/octet-stream', ...auth });
      return json(res, 200, { etag: blob.etag });
    }
    if (req.method === 'DELETE') { await del(path, auth); return json(res, 200, { ok: true }); }
    return json(res, 405, { error: 'Method not allowed' });
  } catch (error) {
    const conflict = /Precondition|AlreadyExists|already exists/.test(error.name + ' ' + error.message);
    console.error('Blob operation failed:', error.name, /No blob credentials/.test(error.message) ? 'missing-credentials' : /oidc|token/i.test(error.message) ? 'authentication' : 'storage-error');
    if (!res.headersSent) json(res, conflict ? 412 : 502, { error: conflict ? 'Conflict' : 'Storage unavailable' });
    else res.destroy();
  }
});
server.listen(8081, '127.0.0.1', () => {
  const child = spawn('dotnet', ['LeitorDeJornal.Web.dll'], { stdio: 'inherit', env: { ...process.env, BlobBridge__Secret: secret, BlobBridge__Url: 'http://127.0.0.1:8081' } });
  child.on('exit', code => { server.close(); process.exit(code ?? 1); });
  process.on('SIGTERM', () => child.kill('SIGTERM'));
  process.on('SIGINT', () => child.kill('SIGINT'));
});
