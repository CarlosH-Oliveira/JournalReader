'use strict';
/*
 * Composição é uma projeção descartável. O servidor só recebe offsets UTF-16 e preferências.
 * CSS mantém quatro colunas de altura finita; cada grupo de quatro representa uma folha.
 * O texto fica uma única vez no DOM, preservando a ordem de leitura assistiva.
 */
(async function () {
    const root = document.getElementById('reader');
    if (!root) return;
    const $ = id => document.getElementById(id);
    const id = root.dataset.id;
    const base = root.dataset.base || '/Reader';
    const token = document.querySelector('#csrf-form input[name="__RequestVerificationToken"]').value;
    const textElement = $('reading-text'), paper = $('paper'), viewport = $('text-window');
    const errorBox = $('reader-error');
    let book, paragraphs = [], page = 0, pages = 1, position = 0, timer, editing = null;
    let queue = Promise.resolve(), conflict = false, ready = false, pendingProgress = false, inFlight = 0;
    const stride = 1160; // 4 × (266px de coluna + 24px de intervalo).
    function error(message) { errorBox.hidden = false; errorBox.querySelector('span').textContent = message; $('save-status').textContent = 'Não salvo'; }
    async function request(action, payload) {
        const response = await fetch(`${base}/${action}/${id}`, {
            method: payload === undefined ? 'GET' : 'POST',
            headers: payload === undefined ? {} : { 'Content-Type': 'application/json', 'RequestVerificationToken': token },
            body: payload === undefined ? undefined : JSON.stringify(payload)
        });
        if (!response.ok) {
            let message = 'Não foi possível salvar ou carregar. Verifique a conexão e tente novamente.';
            try { const data = await response.json(); message = data.error || message; } catch { /* Erros do servidor podem não conter JSON. */ }
            if (response.status === 409) conflict = true;
            throw new Error(message);
        }
        return response.json();
    }
    // Uma fila mantém a versão otimista consistente mesmo quando há várias ações rápidas.
    function mutate(action, payload) {
        inFlight++;
        const operation = queue.then(async () => {
            if (conflict) throw new Error('A obra foi alterada em outra aba. Recarregue antes de salvar.');
            $('save-status').textContent = 'Salvando…';
            const result = await request(action, { ...payload, version: book.version });
            book.version = result.version;
            errorBox.hidden = true;
            $('save-status').textContent = 'Salvo no acervo';
        });
        const tracked = operation.finally(() => { inFlight--; });
        queue = tracked.catch(() => {});
        return tracked;
    }
    function progressPayload() {
        return { position, theme: $('theme').value, fontSize: Number($('font-size').value), accessible: $('accessible').checked };
    }
    function scheduleSave() {
        if (!ready) return;
        pendingProgress = true;
        $('save-status').textContent = 'Alterações pendentes…';
        clearTimeout(timer);
        timer = setTimeout(saveProgress, 500);
    }
    async function saveProgress() {
        clearTimeout(timer);
        if (!book || !pendingProgress) return;
        const payload = progressPayload();
        pendingProgress = false;
        try { await mutate('Progress', payload); }
        catch (ex) { pendingProgress = true; error(ex.message); }
    }
    $('retry-save').addEventListener('click', () => { pendingProgress = true; saveProgress(); });
    $('reload-reader').addEventListener('click', () => location.reload());

    function renderText() {
        const fragment = document.createDocumentFragment();
        paragraphs = [];
        let start = 0;
        // Separadores fazem parte dos offsets canônicos; não são inseridos como texto em outro bloco.
        for (const value of book.text.split('\n\n')) {
            const p = document.createElement('p');
            const end = start + value.length;
            p.dataset.start = String(start);
            const annotations = book.annotations.filter(a => a.kind !== 'bookmark' && a.end > start && a.start < end);
            const bounds = [...new Set([0, value.length, ...annotations.flatMap(a => [Math.max(0, a.start - start), Math.min(value.length, a.end - start)])])].sort((a, b) => a - b);
            for (let i = 0; i < bounds.length - 1; i++) {
                const text = value.slice(bounds[i], bounds[i + 1]);
                const annotation = annotations.find(a => a.start <= start + bounds[i] && a.end >= start + bounds[i + 1]);
                if (annotation) {
                    const mark = document.createElement('mark');
                    mark.className = annotation.color;
                    mark.textContent = text;
                    mark.title = annotation.note || 'Destaque';
                    p.append(mark);
                } else p.append(document.createTextNode(text));
            }
            if (!value.length) p.append(document.createTextNode(''));
            fragment.append(p);
            paragraphs.push({ element: p, start, end, length: value.length });
            start = end + 2;
        }
        textElement.replaceChildren(fragment);
    }
    // Retorna um nó de texto e offset local, mesmo se houver <mark> entre os nós.
    function nodeAt(offset) {
        offset = Math.min(book.text.length, Math.max(0, offset));
        let low = 0, high = paragraphs.length - 1;
        while (low < high) {
            const mid = Math.ceil((low + high) / 2);
            if (paragraphs[mid].start <= offset) low = mid; else high = mid - 1;
        }
        const p = paragraphs[low];
        let local = Math.min(offset - p.start, p.length);
        const walker = document.createTreeWalker(p.element, NodeFilter.SHOW_TEXT);
        let node = walker.nextNode(), last = node;
        while (node) {
            last = node;
            if (local <= node.length) return { node, offset: Math.max(0, local), paragraph: p };
            local -= node.length;
            node = walker.nextNode();
        }
        return { node: last || p.element, offset: last ? last.length : 0, paragraph: p };
    }
    function rectAt(offset) {
        const location = nodeAt(offset), range = document.createRange();
        range.setStart(location.node, location.offset);
        range.collapse(true);
        let rect = range.getBoundingClientRect();
        if (rect.height === 0) rect = location.paragraph.element.getBoundingClientRect();
        return rect;
    }
    function offsetPage(offset) {
        const rect = rectAt(offset);
        const x = rect.left - viewport.getBoundingClientRect().left + page * stride;
        return Math.max(0, Math.floor((x + 1) / stride));
    }
    function firstOffset(targetPage) {
        // A coordenada X é monotônica na sequência das colunas, inclusive entre folhas.
        let low = 0, high = book.text.length;
        while (low < high) {
            const mid = Math.floor((low + high) / 2);
            if (offsetPage(mid) < targetPage) low = mid + 1; else high = mid;
        }
        return low;
    }
    function updateLabels() {
        const accessible = $('accessible').checked;
        const percent = Math.min(100, Math.floor(100 * position / Math.max(1, book.text.length)));
        $('page-label').textContent = accessible ? 'Leitura em uma coluna' : `Folha ${page + 1} de ${pages}`;
        $('paper-page').textContent = accessible ? 'MODO ACESSÍVEL' : `${page + 1} / ${pages}`;
        $('progress-label').textContent = `${percent}% do texto · posição ${position.toLocaleString('pt-BR')}`;
        $('previous').disabled = accessible || page === 0;
        $('next').disabled = accessible || page >= pages - 1;
    }
    function transform() { textElement.style.transform = $('accessible').checked ? 'none' : `translateX(${-page * stride}px)`; }
    function goTo(offset, save = true) {
        position = Math.min(book.text.length, Math.max(0, offset));
        if ($('accessible').checked) {
            const rect = rectAt(position);
            window.scrollBy({ top: rect.top - 120, behavior: 'instant' });
        } else {
            page = Math.min(pages - 1, offsetPage(position));
            transform();
        }
        updateLabels();
        if (save) scheduleSave();
    }
    function layout() {
        paper.className = 'paper ' + $('theme').value + ($('accessible').checked ? ' accessible' : '');
        textElement.style.fontSize = `${$('font-size').value}px`;
        const anchor = position;
        page = 0; transform();
        pages = Math.max(1, Math.ceil((textElement.scrollWidth + 24) / stride));
        goTo(anchor, false);
    }
    function turn(direction) {
        if ($('accessible').checked) return;
        const target = Math.max(0, Math.min(pages - 1, page + direction));
        if (target === page) return;
        position = firstOffset(target);
        page = target; transform(); updateLabels(); scheduleSave();
        $('paper-scroll').scrollLeft = 0;
    }
    $('previous').addEventListener('click', () => turn(-1));
    $('next').addEventListener('click', () => turn(1));
    document.addEventListener('keydown', event => {
        if (document.querySelector('dialog[open]') || /INPUT|TEXTAREA|SELECT|BUTTON/.test(event.target.tagName) || event.ctrlKey || event.altKey || event.metaKey) return;
        if (['ArrowRight', 'PageDown', 'ArrowLeft', 'PageUp'].includes(event.key) && !$('accessible').checked) {
            event.preventDefault(); turn(['ArrowRight', 'PageDown'].includes(event.key) ? 1 : -1);
        }
    });
    ['theme', 'font-size', 'accessible'].forEach(name => $(name).addEventListener('change', () => {
        $('font-size').value = String(Math.min(32, Math.max(14, Number($('font-size').value) || 18)));
        layout(); scheduleSave();
    }));
    window.addEventListener('resize', () => { if (ready) layout(); });
    let scrollTimer;
    window.addEventListener('scroll', () => {
        if (!ready || !$('accessible').checked || document.querySelector('dialog[open]')) return;
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(() => {
            let low = 0, high = book.text.length;
            while (low < high) { const mid = Math.floor((low + high) / 2); if (rectAt(mid).bottom < 120) low = mid + 1; else high = mid; }
            position = low; updateLabels(); scheduleSave();
        }, 180);
    }, { passive: true });

    function show(name) { $(name).showModal(); }
    function goButton(title, offset, dialog) {
        const button = document.createElement('button');
        button.type = 'button'; button.className = 'result-item'; button.textContent = title;
        button.addEventListener('click', () => { $(dialog).close(); goTo(offset); });
        return button;
    }
    $('open-contents').addEventListener('click', () => {
        const list = $('contents-list'); list.replaceChildren();
        if (!book.contents.length) list.textContent = 'Esta obra não contém um sumário extraível.';
        book.contents.forEach(h => list.append(goButton(h.title, h.offset, 'contents-dialog')));
        show('contents-dialog');
    });
    $('open-search').addEventListener('click', () => show('search-dialog'));
    $('text-search').addEventListener('submit', async event => {
        event.preventDefault();
        const status = $('search-status'), list = $('search-results');
        status.textContent = 'Buscando…'; list.replaceChildren();
        try {
            const response = await fetch(`${base}/Search/${id}?q=${encodeURIComponent($('search-query').value)}`);
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Falha na busca.');
            status.textContent = `${result.length} resultado(s)${result.length === 100 ? ' · limite de 100 por busca' : ''}.`;
            result.forEach(hit => list.append(goButton(hit.excerpt, hit.offset, 'search-dialog')));
        } catch (ex) { status.textContent = ex.message; }
    });
    function selectionOffset(node, local) {
        const p = (node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement).closest('p[data-start]');
        if (!p || !textElement.contains(p)) return null;
        const range = document.createRange(); range.selectNodeContents(p); range.setEnd(node, local);
        return Number(p.dataset.start) + range.toString().length;
    }
    function selectedRange() {
        const selection = window.getSelection();
        if (!selection.rangeCount || selection.isCollapsed) return null;
        const range = selection.getRangeAt(0);
        const start = selectionOffset(range.startContainer, range.startOffset);
        const end = selectionOffset(range.endContainer, range.endOffset);
        return start === null || end === null || start === end ? null : { start, end };
    }
    // Guardar a seleção antes que o clique no botão mova o foco do texto.
    let rememberedSelection = null;
    document.addEventListener('selectionchange', () => { const selected = selectedRange(); if (selected) rememberedSelection = selected; });
    function editAnnotation(annotation) {
        editing = { ...annotation };
        $('selected-quote').textContent = book.text.slice(editing.start, Math.min(editing.end, editing.start + 1000));
        $('note-text').value = editing.note;
        $('note-color').value = editing.color;
        $('note-status').textContent = '';
        $('note-dialog-title').textContent = editing.kind === 'bookmark' ? 'Editar marcador' : 'Anotar trecho';
        show('edit-note-dialog');
    }
    function beginAnnotation(kind) {
        const selected = selectedRange() || rememberedSelection;
        if (!selected) { error('Selecione um trecho do texto antes de destacar ou anotar.'); return; }
        editAnnotation({ id: crypto.randomUUID(), kind, ...selected, note: '', color: 'yellow' });
    }
    $('highlight-selection').addEventListener('click', () => beginAnnotation('highlight'));
    $('note-selection').addEventListener('click', () => beginAnnotation('note'));
    $('add-bookmark').addEventListener('click', async () => {
        const annotation = { id: crypto.randomUUID(), kind: 'bookmark', start: position, end: position, note: 'Posição marcada', color: 'yellow' };
        try { await mutate('Annotate', { annotation }); book.annotations.push(annotation); }
        catch (ex) { error(ex.message); }
    });
    $('note-form').addEventListener('submit', async event => {
        event.preventDefault();
        const annotation = { ...editing, note: $('note-text').value, color: $('note-color').value };
        const submit = event.target.querySelector('[type="submit"]'); submit.disabled = true;
        try {
            await mutate('Annotate', { annotation });
            const index = book.annotations.findIndex(a => a.id === annotation.id);
            if (index >= 0) book.annotations[index] = annotation; else book.annotations.push(annotation);
            $('edit-note-dialog').close(); renderText(); layout();
        } catch (ex) { $('note-status').textContent = ex.message + ' Seu rascunho foi mantido; tente novamente.'; }
        finally { submit.disabled = false; }
    });
    function notesList() {
        const list = $('notes-list'); list.replaceChildren();
        if (!book.annotations.length) list.textContent = 'Ainda não há marcações. Marque uma posição ou selecione um trecho para começar.';
        [...book.annotations].sort((a, b) => a.start - b.start).forEach(annotation => {
            const item = document.createElement('div'); item.className = 'result-item';
            const title = document.createElement('strong');
            title.textContent = annotation.kind === 'bookmark' ? '☆ Marcador' : annotation.kind === 'highlight' ? 'Destaque' : 'Nota';
            const quote = document.createElement('p'); quote.textContent = book.text.slice(annotation.start, Math.min(annotation.end || annotation.start + 100, annotation.start + 180));
            const note = document.createElement('p'); note.textContent = annotation.note;
            const go = goButton('Ir ao trecho →', annotation.start, 'notes-dialog'); go.className = 'button small';
            const edit = document.createElement('button'); edit.type = 'button'; edit.className = 'button small'; edit.textContent = 'Editar';
            edit.addEventListener('click', () => { $('notes-dialog').close(); editAnnotation(annotation); });
            const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'button small'; remove.textContent = 'Remover';
            remove.addEventListener('click', async () => {
                remove.disabled = true;
                try { await mutate('RemoveAnnotation', { annotationId: annotation.id }); book.annotations = book.annotations.filter(a => a.id !== annotation.id); renderText(); layout(); notesList(); }
                catch (ex) { error(ex.message); remove.disabled = false; }
            });
            item.append(title, quote, note, go, edit, remove); list.append(item);
        });
    }
    $('open-notes').addEventListener('click', () => { notesList(); show('notes-dialog'); });
    // Salvar ao ocultar reduz perdas. O evento unload não garante commit; nunca anunciar sucesso antecipadamente.
    document.addEventListener('visibilitychange', () => { if (document.hidden) saveProgress(); });
    window.addEventListener('beforeunload', event => {
        if (pendingProgress || inFlight > 0 || $('edit-note-dialog').open) { event.preventDefault(); event.returnValue = ''; }
    });
    try {
        book = await request('Data');
        position = book.position;
        $('theme').value = book.preferences.theme;
        $('font-size').value = String(book.preferences.fontSize);
        $('accessible').checked = book.preferences.accessible;
        await document.fonts.ready;
        renderText(); layout(); ready = true;
        // Também registra a abertura da obra para ordenar as leituras recentes.
        scheduleSave();
    } catch (ex) { error(ex.message); }
})();
