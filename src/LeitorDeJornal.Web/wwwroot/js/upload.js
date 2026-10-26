'use strict';
// O corpo grande vai diretamente ao Blob privado. A função recebe só metadados.
for (const form of document.querySelectorAll('[data-direct-upload="true"]')) {
    form.addEventListener('submit', async event => {
        event.preventDefault();
        const file = form.querySelector('input[type="file"]').files[0];
        const status = form.querySelector('[data-upload-status]');
        const button = form.querySelector('button[type="submit"]');
        if (!file || file.size === 0 || file.size > 50 * 1024 * 1024) {
            status.textContent = 'Selecione um arquivo de até 50 MiB.'; return;
        }
        button.disabled = true;
        try {
            const token = form.querySelector('input[name="__RequestVerificationToken"]').value;
            status.textContent = 'Preparando envio seguro…';
            const response = await fetch('/Import/PrepareBlob', { method: 'POST',
                body: new URLSearchParams({ filename: file.name, size: String(file.size), __RequestVerificationToken: token }) });
            if (!response.ok) throw new Error('Não foi possível autorizar o envio. Recarregue a página e tente novamente.');
            const ticket = await response.json();
            const uploadUrl = new URL(ticket.uploadUrl);
            if (uploadUrl.protocol !== 'https:' || !(uploadUrl.hostname === 'blob.vercel-storage.com' || uploadUrl.hostname.endsWith('.blob.vercel-storage.com'))) throw new Error('Endereço de envio inválido.');
            status.textContent = 'Enviando arquivo diretamente ao armazenamento privado…';
            await new Promise((resolve, reject) => {
                const xhr = new XMLHttpRequest();
                xhr.open('PUT', uploadUrl.href);
                xhr.setRequestHeader('Content-Type', 'application/octet-stream');
                xhr.timeout = 15 * 60 * 1000;
                xhr.upload.onprogress = e => { if (e.lengthComputable) status.textContent = `Enviando arquivo: ${Math.round(e.loaded / e.total * 100)}%`; };
                xhr.onload = () => xhr.status >= 200 && xhr.status < 300 ? resolve() : reject(new Error('O armazenamento recusou o arquivo. Tente novamente.'));
                xhr.onerror = () => reject(new Error('Falha de conexão durante o envio. Tente novamente.'));
                xhr.ontimeout = () => reject(new Error('O envio demorou demais. Tente novamente.'));
                xhr.send(file);
            });
            status.textContent = 'Arquivo enviado. Extraindo o texto e preparando a prévia…';
            const finish = document.createElement('form');
            finish.method = 'POST'; finish.action = '/Import/FromBlob';
            for (const [name, value] of Object.entries({ path: ticket.path, filename: file.name, __RequestVerificationToken: token })) {
                const input = document.createElement('input'); input.type = 'hidden'; input.name = name; input.value = value; finish.append(input);
            }
            document.body.append(finish); finish.submit();
        } catch (error) { status.textContent = error.message || 'Falha no envio. Tente novamente.'; button.disabled = false; }
    });
}
