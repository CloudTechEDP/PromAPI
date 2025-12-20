// Elementos principais
const modal = document.getElementById('modal');
const modalContent = document.getElementById('modal-content');
// Obtém o botão de fechar dentro do modalContent para garantir que ele exista
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

    // 3. Listener para copiar texto CURL nos elementos pré-existentes
    document.querySelectorAll('pre.curl-text').forEach(pre => pre.addEventListener('click', () => copyToClipboard(pre)));

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

    modalContent.appendChild(detailsClone);

    // Adiciona o listener para copiar o CURL DENTRO da modal (conteúdo clonado)
    modalContent.querySelectorAll('pre.curl-text').forEach(pre => pre.addEventListener('click', () => copyToClipboard(pre)));

    // Atualiza o aria-label do modal
    const metricNameText = nameElement.textContent.trim();
    modal.setAttribute('aria-label', `Detalhes da métrica: ${metricNameText}`);
    
    // Exibe a modal
    modal.classList.add('show');
    modal.setAttribute('aria-hidden', 'false');
}

/**
 * Fecha a modal.
 */
function closeModal() {
    if (!modal) return;
    modal.classList.remove('show');
    modal.setAttribute('aria-hidden', 'true');
}

/**
 * Exibe o feedback visual de sucesso na cópia.
 * @param {HTMLElement} preElement - O elemento <pre> onde o feedback será exibido.
 */
function handleCopySuccess(preElement) {
    // 1. Cria ou exibe o feedback visual
    let feedback = preElement.querySelector('.copy-feedback');
    if (!feedback) {
        feedback = document.createElement('span');
        feedback.classList.add('copy-feedback');
        preElement.appendChild(feedback);
    }
    feedback.textContent = 'Copiado!';
    
    // Ativa o display do feedback
    feedback.classList.add('show');

    // 2. Remove o feedback após 1.2 segundos
    setTimeout(() => {
        feedback.classList.remove('show');
    }, 1200);
}

/**
 * Método de fallback para cópia usando document.execCommand.
 * @param {HTMLElement} preElement - O elemento <pre> a ser copiado.
 * @param {string} text - O texto a ser copiado.
 */
function handleCopyFallback(preElement, text) {
    // Cria um textarea temporário, copia, e remove.
    const tempTextarea = document.createElement('textarea');
    tempTextarea.value = text;
    // Estilos para evitar problemas de visualização ou rolagem
    tempTextarea.style.position = 'fixed'; 
    tempTextarea.style.opacity = '0';
    document.body.appendChild(tempTextarea);
    
    tempTextarea.focus();
    tempTextarea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            handleCopySuccess(preElement);
        } else {
            alert('Não foi possível copiar automaticamente. Por favor, pressione Ctrl+C / Cmd+C.');
        }
    } catch (err) {
        console.error('Fallback copy failed', err);
        alert('Falha total ao copiar. Por favor, pressione Ctrl+C / Cmd+C.');
    }

    document.body.removeChild(tempTextarea);
}


/**
 * Copia o conteúdo de um elemento <pre> para a área de transferência e dá feedback visual.
 * @param {HTMLElement} preElement - O elemento <pre> a ser copiado.
 */
function copyToClipboard(preElement) {
    if (!preElement || !preElement.textContent) {
        alert('O elemento de texto está vazio.');
        return;
    }
    
    const text = preElement.textContent.trim();
    
    // 1. Tenta usar a API moderna (navigator.clipboard)
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            handleCopySuccess(preElement);
        }).catch(() => {
            // Se falhar (ex: file:// context), tenta o fallback
            handleCopyFallback(preElement, text);
        });
    } else {
        // 2. Se a API não existir, tenta o fallback
        handleCopyFallback(preElement, text);
    }
}