'use strict';
// <dialog> oferece foco contido, Escape e restauração de foco nativos do navegador.
document.querySelectorAll('[data-open-dialog]').forEach(button => button.addEventListener('click', () => {
    document.getElementById(button.dataset.openDialog).showModal();
}));
document.querySelectorAll('[data-close-dialog]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
document.querySelectorAll('[data-upload-form]').forEach(form => form.addEventListener('submit', () => {
    if (form.dataset.directUpload === 'true') return;
    const status = form.querySelector('[data-upload-status]');
    if (status) status.textContent = 'Processando arquivo. Aguarde a conclusão…';
    form.querySelector('button[type="submit"]').disabled = true;
}));
