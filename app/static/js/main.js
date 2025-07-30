// JavaScript principal pour Stock Manager

document.addEventListener('DOMContentLoaded', function() {
    // Initialiser toutes les fonctionnalités
    initializeTooltips();
    initializeAlerts();
    initializeFormValidation();
    initializeSearchFeatures();
    initializeStockAlerts();
    initializeDashboardAnimations();
});

// Initialiser les tooltips Bootstrap
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Gestion des alertes auto-dismiss
function initializeAlerts() {
    // Auto-dismiss des alertes après 5 secondes
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
}

// Validation des formulaires en temps réel
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Validation en temps réel pour les champs de prix
    const priceInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    priceInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value < 0) {
                this.setCustomValidity('Le prix ne peut pas être négatif');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Validation pour les quantités
    const quantityInputs = document.querySelectorAll('input[name="quantity"], input[name="quantity_sold"]');
    quantityInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value < 0) {
                this.setCustomValidity('La quantité ne peut pas être négative');
            } else {
                this.setCustomValidity('');
            }
        });
    });
}

// Fonctionnalités de recherche améliorées
function initializeSearchFeatures() {
    const searchInput = document.getElementById('search_query');
    if (searchInput) {
        // Recherche en temps réel (avec debounce)
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                // Ici on pourrait implémenter une recherche AJAX
                // Pour l'instant, on se contente de valider la saisie
                if (searchInput.value.length > 0 && searchInput.value.length < 2) {
                    searchInput.setCustomValidity('Tapez au moins 2 caractères');
                } else {
                    searchInput.setCustomValidity('');
                }
            }, 300);
        });
    }

    // Highlight des résultats de recherche
    const searchQuery = new URLSearchParams(window.location.search).get('search_query');
    if (searchQuery) {
        highlightSearchResults(searchQuery);
    }
}

// Surligner les résultats de recherche
function highlightSearchResults(query) {
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(function(row) {
        const textContent = row.textContent.toLowerCase();
        if (textContent.includes(query.toLowerCase())) {
            row.classList.add('table-warning');
        }
    });
}

// Gestion des alertes de stock faible
function initializeStockAlerts() {
    const stockBadges = document.querySelectorAll('.badge.bg-danger, .badge.bg-warning');
    stockBadges.forEach(function(badge) {
        const quantity = parseInt(badge.textContent);
        if (quantity === 0) {
            badge.textContent = 'RUPTURE';
            badge.classList.add('animate__animated', 'animate__pulse', 'animate__infinite');
        } else if (quantity < 5) {
            badge.classList.add('animate__animated', 'animate__heartBeat');
        }
    });
}

// Animations pour le dashboard
function initializeDashboardAnimations() {
    const dashboardCards = document.querySelectorAll('.dashboard-card, .card');
    
    // Observer pour les animations au scroll
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        });

        dashboardCards.forEach(function(card) {
            observer.observe(card);
        });
    }
}

// Fonction pour confirmer la suppression
function confirmDelete(itemName, deleteUrl, itemType = 'élément') {
    const message = `Êtes-vous sûr de vouloir supprimer ${itemType} "${itemName}" ?\n\nCette action est irréversible.`;
    
    if (confirm(message)) {
        // Créer un formulaire pour la suppression
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = deleteUrl;
        
        // Ajouter le token CSRF si disponible
        const csrfToken = document.querySelector('meta[name=csrf-token]');
        if (csrfToken) {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrf_token';
            csrfInput.value = csrfToken.getAttribute('content');
            form.appendChild(csrfInput);
        }
        
        // Ajouter un indicateur de chargement
        const deleteButton = event.target.closest('button');
        if (deleteButton) {
            deleteButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Suppression...';
            deleteButton.disabled = true;
        }
        
        document.body.appendChild(form);
        form.submit();
    }
}

// Fonction pour formater les prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

// Fonction pour formater les dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Gestion des formulaires de vente
function initializeSalesForm() {
    const productSelect = document.getElementById('product_id');
    const quantityInput = document.getElementById('quantity_sold');
    const totalInput = document.getElementById('totalPrice');
    
    if (productSelect && quantityInput && totalInput) {
        function updateTotal() {
            const selectedOption = productSelect.options[productSelect.selectedIndex];
            if (selectedOption && selectedOption.value) {
                // Extraire le prix du texte de l'option (à améliorer avec des données JSON)
                const quantity = parseFloat(quantityInput.value) || 0;
                // Le calcul du total sera fait côté serveur pour plus de sécurité
                totalInput.value = quantity > 0 ? 'Calculé automatiquement' : '';
            } else {
                totalInput.value = '';
            }
        }
        
        productSelect.addEventListener('change', updateTotal);
        quantityInput.addEventListener('input', updateTotal);
    }
}

// Fonction pour copier du texte dans le presse-papiers
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showNotification('Copié dans le presse-papiers !', 'success');
        });
    } else {
        // Fallback pour les navigateurs plus anciens
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Copié dans le presse-papiers !', 'success');
    }
}

// Système de notifications toast
function showNotification(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Nettoyer après fermeture
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Créer ou récupérer le conteneur de toasts
function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    return container;
}

// Gestion du mode sombre (pour une future implémentation)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
}

// Charger le mode sombre depuis localStorage
function loadDarkMode() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
    }
}

// Fonction utilitaire pour débouncer les événements
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Fonction pour valider les emails
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Fonction pour valider les numéros de téléphone français
function isValidPhoneNumber(phone) {
    const phoneRegex = /^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/;
    return phoneRegex.test(phone);
}

// Export des fonctions pour utilisation dans d'autres scripts
window.StockManager = {
    confirmDelete,
    formatPrice,
    formatDate,
    copyToClipboard,
    showNotification,
    toggleDarkMode,
    debounce,
    isValidEmail,
    isValidPhoneNumber
};