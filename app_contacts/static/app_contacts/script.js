// Script para melhorar a experiência com teclado e acessibilidade
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona navegação por teclado aprimorada
    const actionButtons = document.querySelectorAll('.btn');
    
    actionButtons.forEach(button => {
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // Anúncio para leitores de tela sobre a quantidade de contatos
    const statusEl = document.getElementById('status-announcements');
    const contactRows = document.querySelectorAll('tbody tr');
    const contactCount = contactRows.length;
    
    if (contactCount > 0) {
        statusEl.textContent = `${contactCount} contato${contactCount !== 1 ? 's' : ''} encontrado${contactCount !== 1 ? 's' : ''}`;
    } else {
        statusEl.textContent = 'Nenhum contato encontrado';
    }
    
    // Adiciona confirmação acessível para exclusão
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const contactName = this.getAttribute('aria-label').replace('Excluir contato ', '');
            const confirmMessage = `Tem certeza que deseja excluir o contato ${contactName}? Esta ação não pode ser desfeita.`;
            
            if (!confirm(confirmMessage)) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Melhora a navegação por teclado na tabela
    const tableRows = document.querySelectorAll('.contacts-table tbody tr');
    tableRows.forEach((row, index) => {
        row.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowDown' && index < tableRows.length - 1) {
                tableRows[index + 1].querySelector('.btn').focus();
            } else if (e.key === 'ArrowUp' && index > 0) {
                tableRows[index - 1].querySelector('.btn').focus();
            }
        });
    });
    
    // Adiciona feedback sonoro para leitores de tela em ações
    function announceAction(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'assertive');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;
        document.body.appendChild(announcement);
        
        // Remove o elemento após um tempo para não acumular
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }
    
    // Anuncia quando botões recebem foco
    actionButtons.forEach(button => {
        button.addEventListener('focus', function() {
            const action = this.classList.contains('btn-edit') ? 'Editar' : 'Excluir';
            const contactName = this.getAttribute('aria-label').split(' ').slice(-1)[0];
            announceAction(`Botão ${action} para ${contactName} selecionado`);
        });
    });
});