// Animations générales
document.addEventListener('DOMContentLoaded', function() {
    // Animation des éléments au chargement
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    });

    animateElements.forEach(element => {
        observer.observe(element);
    });

    // Gestion des notifications
    const notificationDropdown = document.querySelector('.notification-dropdown');
    if (notificationDropdown) {
        const notificationToggle = document.querySelector('.notification-toggle');
        const notificationCount = document.querySelector('.notification-count');
        let isOpen = false;

        notificationToggle.addEventListener('click', function(e) {
            e.preventDefault();
            isOpen = !isOpen;
            notificationDropdown.classList.toggle('show');
            
            if (isOpen) {
                // Marquer les notifications comme lues
                const unreadNotifications = document.querySelectorAll('.notification-item.unread');
                unreadNotifications.forEach(notification => {
                    notification.classList.remove('unread');
                });
                
                // Mettre à jour le compteur
                if (notificationCount) {
                    notificationCount.textContent = '0';
                    notificationCount.classList.add('d-none');
                }
            }
        });

        // Fermer le dropdown en cliquant en dehors
        document.addEventListener('click', function(e) {
            if (!notificationToggle.contains(e.target) && !notificationDropdown.contains(e.target)) {
                notificationDropdown.classList.remove('show');
                isOpen = false;
            }
        });
    }

    // Gestion des formulaires
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        // Validation en temps réel
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                validateInput(this);
            });
            
            input.addEventListener('blur', function() {
                validateInput(this);
            });
        });

        // Soumission du formulaire
        form.addEventListener('submit', function(e) {
            let isValid = true;
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                showFormError(form, 'Veuillez corriger les erreurs dans le formulaire.');
            }
        });
    });

    // Gestion des cartes interactives
    const cards = document.querySelectorAll('.interactive-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover');
        });
    });
});

// Fonctions utilitaires
function validateInput(input) {
    const isValid = input.checkValidity();
    const formGroup = input.closest('.form-group');
    
    if (formGroup) {
        if (isValid) {
            formGroup.classList.remove('is-invalid');
            formGroup.classList.add('is-valid');
        } else {
            formGroup.classList.remove('is-valid');
            formGroup.classList.add('is-invalid');
        }
    }
    
    return isValid;
}

function showFormError(form, message) {
    const errorDiv = form.querySelector('.form-error') || document.createElement('div');
    errorDiv.className = 'alert alert-danger form-error mt-3';
    errorDiv.textContent = message;
    
    if (!form.querySelector('.form-error')) {
        form.insertBefore(errorDiv, form.firstChild);
    }
}

// Animations de chargement
function showLoading(element) {
    const loader = document.createElement('div');
    loader.className = 'loader';
    element.appendChild(loader);
    element.classList.add('loading');
}

function hideLoading(element) {
    const loader = element.querySelector('.loader');
    if (loader) {
        loader.remove();
    }
    element.classList.remove('loading');
}

// Gestion des messages flash
function showFlashMessage(message, type = 'success') {
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    const flashMessage = document.createElement('div');
    flashMessage.className = `alert alert-${type} flash-message`;
    flashMessage.textContent = message;
    
    flashContainer.appendChild(flashMessage);
    
    setTimeout(() => {
        flashMessage.classList.add('fade-out');
        setTimeout(() => {
            flashMessage.remove();
        }, 300);
    }, 3000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.insertBefore(container, document.body.firstChild);
    return container;
}

// Gestion des modales
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
        document.body.classList.add('modal-open');
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
    }
}

// Export des fonctions pour utilisation dans d'autres fichiers
window.appUtils = {
    validateInput,
    showFormError,
    showLoading,
    hideLoading,
    showFlashMessage,
    showModal,
    hideModal
}; 