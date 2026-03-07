// AnytimeEsim - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initSearch();
    initFilters();
    initBuyButtons();
    initScrollAnimations();
});

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.querySelector('.search-container .btn');
    
    if (searchInput) {
        // Real-time search
        searchInput.addEventListener('input', debounce(function(e) {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                performSearch(query);
            } else if (query.length === 0) {
                // Clear search results and show all plans
                window.location.href = '/';
            }
        }, 300));
        
        // Search on button click
        if (searchButton) {
            searchButton.addEventListener('click', function() {
                const query = searchInput.value.trim();
                if (query.length > 0) {
                    performSearch(query);
                }
            });
        }
        
        // Search on Enter key
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = e.target.value.trim();
                if (query.length > 0) {
                    performSearch(query);
                }
            }
        });
    }
}

// Filter functionality
function initFilters() {
    const countryFilter = document.getElementById('country-filter');
    const priceFilter = document.getElementById('price-filter');
    const resetBtn = document.getElementById('reset-filters');
    
    if (countryFilter) {
        countryFilter.addEventListener('change', applyFilters);
    }
    
    if (priceFilter) {
        priceFilter.addEventListener('change', applyFilters);
    }
    
    if (resetBtn) {
        resetBtn.addEventListener('click', resetFilters);
    }
}

// Buy button functionality
function initBuyButtons() {
    const buyButtons = document.querySelectorAll('.buy-btn');
    
    buyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const planId = this.getAttribute('data-plan-id');
            const planName = this.closest('.product-card').querySelector('.product-title').textContent;
            const planPrice = this.closest('.product-card').querySelector('.product-price').textContent;
            
            showBuyModal(planId, planName, planPrice);
        });
    });
}

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all fade-in elements
    document.querySelectorAll('.fade-in').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Search implementation
function performSearch(query) {
    // For now, redirect to home with search parameter
    // In a full implementation, this would make an AJAX call
    window.location.href = `/?search=${encodeURIComponent(query)}`;
}

// Filter implementation
function applyFilters() {
    const country = document.getElementById('country-filter').value;
    const price = document.getElementById('price-filter').value;
    
    let url = '?';
    if (country) url += `country=${country}&`;
    if (price) url += `price=${price}&`;
    
    window.location.href = url;
}

// Reset filters
function resetFilters() {
    const countryFilter = document.getElementById('country-filter');
    const priceFilter = document.getElementById('price-filter');
    
    if (countryFilter) countryFilter.value = '';
    if (priceFilter) priceFilter.value = '';
    
    window.location.href = '/';
}

// Buy modal (placeholder for actual implementation)
function showBuyModal(planId, planName, planPrice) {
    // Create modal HTML
    const modalHTML = `
        <div class="modal fade" id="buyModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Purchase ${planName}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Plan:</strong> ${planName}</p>
                        <p><strong>Price:</strong> ${planPrice}</p>
                        <p>This is a demo modal. In a full implementation, this would show a checkout form.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary">Proceed to Checkout</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('buyModal'));
    modal.show();
    
    // Remove modal when hidden
    document.getElementById('buyModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// Utility function for debouncing
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

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Mobile menu toggle
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('navbar-toggler')) {
        const navbar = document.querySelector('.navbar-collapse');
        if (navbar) {
            navbar.classList.toggle('show');
        }
    }
});

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    const navbar = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');
    
    if (navbar && navbar.classList.contains('show') && 
        !navbar.contains(e.target) && !navbarToggler.contains(e.target)) {
        navbar.classList.remove('show');
    }
});