const modal = document.getElementById('modal');
const modalContent = document.getElementById('modal-content');
const modalCloseBtn = modalContent ? modalContent.querySelector('.modal-close') : null;

document.addEventListener('DOMContentLoaded', () => {
    const metricNames = document.querySelectorAll('.metric-name');
    metricNames.forEach(nameEl => {
        nameEl.addEventListener('click', () => {
            openModalWithDetails(nameEl);
        });

        nameEl.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openModalWithDetails(nameEl);
            }
        });
    });

    // 2. Listeners para fechar a modal
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', closeModal);
    }

    // Click no backdrop (fora do modal-content) fecha a modal
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
    }

    // Fecha no Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal && modal.classList.contains('show')) closeModal();
    });

 
    document.querySelectorAll('code').forEach(codeElement => {
        if (codeElement.textContent.includes('http://example.com')) {
            codeElement.textContent = codeElement.textContent.replace('http://example.com', baseUrl);
        }
   
    });

    document.querySelectorAll('pre.curl-text').forEach(preElement => {
        if (preElement.textContent.includes('http://example.com')) {
            preElement.textContent = preElement.textContent.replace('http://example.com', baseUrl);
        }

    });
});

/**
 * Abre a modal com os detalhes da métrica clicada.
 * @param {HTMLElement} nameElement - O elemento .metric-name clicado.
 */
function openModalWithDetails(nameElement) {
    if (!modal || !modalContent) return;

    const card = nameElement.closest('.link-item');
    if (!card) return;
    const details = card.querySelector('.metric-details');
    if (!details) return;

    // Remove qualquer conteúdo prévio (mantém apenas o botão de fechar original)
    const existingClose = modalContent.querySelector('.modal-close');
    modalContent.innerHTML = '';
    if (existingClose) {
        modalContent.appendChild(existingClose);
    }
    
    // Clona os detalhes para a modal
    const detailsClone = details.cloneNode(true);
    detailsClone.style.display = 'block'; 
    detailsClone.removeAttribute('aria-hidden');

    // Quebra de linha automática no exemplo CURL
    const curlPre = detailsClone.querySelector('pre.curl-text');
    if (curlPre) {
        curlPre.style.whiteSpace = 'pre-wrap';
        curlPre.style.wordBreak = 'break-all';
    }

    modalContent.appendChild(detailsClone);

    // Botão copiar (mantém como antes)
    if (curlPre) {
        const copyBtn = document.createElement('button');
        copyBtn.textContent = '📋 Copiar CURL';
        copyBtn.className = 'modal-copy-btn';
        copyBtn.style = `display: block; margin: 5px auto 0 auto; background: #007bff; color: #fff; border: none; border-radius: 50px; padding: 8px 16px; font-size: 14px; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.10); z-index: 20;`;
        copyBtn.addEventListener('click', () => {
            copyTextToClipboard(curlPre.textContent);
            showCopyFeedback(copyBtn);
        });
        modalContent.appendChild(copyBtn);
        modalContent.style.position = 'relative';
    }

    // Atualiza o aria-label do modal
    const metricNameText = nameElement.textContent.trim();
    modal.setAttribute('aria-label', `Detalhes da métrica: ${metricNameText}`);
    
    // Exibe a modal
    modal.classList.add('show');
    modal.setAttribute('aria-hidden', 'false');
}

// Função para copiar texto para a área de transferência
function copyTextToClipboard(text) {
    if (!text) return;
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text.trim());
    } else {
        const tempTextarea = document.createElement('textarea');
        tempTextarea.value = text.trim();
        tempTextarea.style.position = 'fixed';
        tempTextarea.style.opacity = '0';
        document.body.appendChild(tempTextarea);
        tempTextarea.focus();
        tempTextarea.select();
        try {
            document.execCommand('copy');
        } catch (err) {}
        document.body.removeChild(tempTextarea);
    }
}

function showCopyFeedback(btn) {
    let feedback = btn.parentElement.querySelector('.copy-feedback-modal');
    if (!feedback) {
        feedback = document.createElement('span');
        feedback.className = 'copy-feedback-modal';
        feedback.style = 'position: absolute; right: 24px; bottom: 48px; background: #e6ffe6; color: #008000; font-size: 13px; font-weight: 700; border-radius: 6px; padding: 6px 14px; opacity: 0; transition: opacity 0.3s; z-index: 30; pointer-events: none;';
        btn.parentElement.appendChild(feedback);
    }
    feedback.textContent = 'Exemplo copiado!';
    feedback.style.opacity = '1';
    setTimeout(() => {
        feedback.style.opacity = '0';
    }, 1200);
}

/**
 * Fecha a modal.
 */
function closeModal() {
    if (!modal) return;
    modal.classList.remove('show');
    modal.setAttribute('aria-hidden', 'true');
}
