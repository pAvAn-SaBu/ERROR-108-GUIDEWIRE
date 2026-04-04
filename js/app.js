/**
 * REVO | Global App Controller
 * Handles state management, navigation, and common UI logic.
 */

const REVO_STORAGE_KEY = 'revo_app_state';

// Default State
const initialState = {
    user: {
        name: 'Abhin',
        rating: 4.8,
        isVerified: true
    },
    activePlatforms: ['Swiggy', 'Zomato', 'Porter', 'Zepto'], // Pre-selected for immediate high-fidelity demo
    activePolicy: { name: 'Standard', premium: 30, coverage: '₹45,000' }, // Pre-selected for demo
    walletBalance: 0,
    disruptionActive: false,
    payoutHistory: []
};

// State Management
function getState() {
    const saved = localStorage.getItem(REVO_STORAGE_KEY);
    return saved ? JSON.parse(saved) : initialState;
}

function saveState(state) {
    localStorage.setItem(REVO_STORAGE_KEY, JSON.stringify(state));
    // Trigger custom event for reactivity within same page
    window.dispatchEvent(new CustomEvent('revoStateChanged', { detail: state }));
}

function updateState(updates) {
    const newState = { ...getState(), ...updates };
    saveState(newState);
    return newState;
}

/**
 * UI Utilities
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount);
}

/**
 * Navigation Fixer
 * Ensures all links and buttons use correct relative paths
 */
function fixNavigation() {
    const navLinks = document.querySelectorAll('a');
    navLinks.forEach(link => {
        const text = link.innerText.toLowerCase();
        // Remove Sync from all headers
        if (text.includes('sync')) {
            link.style.display = 'none';
            return;
        }
        if (text.includes('home')) link.href = 'landing.html';
        if (text.includes('shield')) link.href = 'index.html';
        if (text.includes('profile') || text.includes('logout')) link.href = 'profile.html'; 
        if (text.includes('plans')) link.href = 'coverage.html';
    });
}

/**
 * Emoji Audit & Fix
 */
function cleanseEmojis() {
    const stars = document.body.innerHTML.match(/★/g);
    if (stars) {
        document.body.innerHTML = document.body.innerHTML.replace(/★/g, '<span class="material-symbols-outlined text-orange-600 text-2xl" style="font-variation-settings: \'FILL\' 1;">star</span>');
    }
}

function initCoverage() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => {
        if (btn.innerText.toLowerCase().includes('select') || btn.innerText.toLowerCase().includes('kinetic')) {
            btn.onclick = () => {
                const card = btn.closest('.bg-surface-container-lowest') || btn.closest('.bg-white');
                if (!card) return;
                const planName = card.querySelector('h2')?.innerText || 'Kinetic';
                const premiumText = card.querySelector('p.text-3xl, p.text-2xl')?.innerText || '₹30';
                const premium = parseInt(premiumText.replace('₹', '') || '0');
                
                updateState({ 
                    activePolicy: { 
                        name: planName, 
                        premium: premium,
                        coverage: '₹45,000'
                    } 
                });
                location.href = 'index.html';
            };
        }
    });
}

function initDashboard() {
    const simTrigger = document.createElement('div');
    simTrigger.style = "position: fixed; top: 10px; right: 10px; width: 10px; height: 10px; background: rgba(0,0,0,0.01); z-index: 9999; cursor: pointer;";
    simTrigger.title = "Simulate Disruption";
    simTrigger.onclick = () => triggerDisruption();
    document.body.appendChild(simTrigger);

    const payoutBtn = document.getElementById('payout-btn');
    if (payoutBtn) {
        payoutBtn.onclick = () => {
            payoutBtn.disabled = true;
            payoutBtn.innerHTML = '<span class="animate-spin material-symbols-outlined text-2xl">refresh</span> Verifying 6-Signal AI...';
            
            setTimeout(() => {
                const signalContainer = document.getElementById('verification-signals');
                if (signalContainer) {
                    signalContainer.innerHTML = `
                        <div class="flex items-center gap-2 px-3 py-1 bg-white rounded-full border border-orange-100 shadow-sm animate-bounce">
                            <span class="material-symbols-outlined text-orange-600 text-[14px]" style="font-variation-settings: 'FILL' 1;">verified</span>
                            <span class="text-[12px] font-bold text-gray-900 uppercase">GPS Verified</span>
                        </div>
                        <div class="flex items-center gap-2 px-3 py-1 bg-white rounded-full border border-orange-100 shadow-sm animate-bounce" style="animation-delay: 0.1s">
                            <span class="material-symbols-outlined text-orange-600 text-[14px]" style="font-variation-settings: 'FILL' 1;">verified</span>
                            <span class="text-[12px] font-bold text-gray-900 uppercase">Latency Sync</span>
                        </div>
                    `;
                }
                
                setTimeout(() => {
                    const state = getState();
                    updateState({ walletBalance: state.walletBalance + 700 });
                    payoutBtn.classList.replace('bg-orange-600', 'bg-orange-100');
                    payoutBtn.classList.replace('text-white', 'text-orange-600');
                    payoutBtn.innerHTML = `<span class="material-symbols-outlined text-orange-600">check_circle</span> ₹700 Added to Wallet`;
                }, 1500);
            }, 2000);
        };
    }
}

function triggerDisruption() {
    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        alertContainer.classList.remove('hidden');
        alertContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    cleanseEmojis();
    fixNavigation();
    
    const path = window.location.pathname;
    // Check for dashboard on index.html (root) too
    if (path.includes('dashboard') || path.endsWith('/') || path.endsWith('index.html')) {
        initDashboard();
    }
    if (path.includes('coverage')) initCoverage();
    if (path.includes('auth')) initAuth();
});

function initAuth() {
    const toggleBtn = document.getElementById('auth-toggle');
    const authTitle = document.getElementById('auth-title');
    const authSubmit = document.getElementById('auth-submit');
    const nameField = document.getElementById('name-field');
    const nameInput = document.getElementById('auth-name');
    const emailInput = document.getElementById('auth-email');
    
    // Start in "Create Account" mode by default
    let isCreateMode = true;

    if (toggleBtn) {
        toggleBtn.onclick = (e) => {
            e.preventDefault();
            isCreateMode = !isCreateMode;
            if (isCreateMode) {
                authTitle.innerText = 'Join the Shield.';
                authSubmit.innerText = 'Create Account';
                toggleBtn.innerText = 'Already have an account? Sign In';
                if (nameField) nameField.style.display = '';
            } else {
                authTitle.innerText = 'Welcome back.';
                authSubmit.innerText = 'Sign In';
                toggleBtn.innerText = 'Need an account? Create Account';
                if (nameField) nameField.style.display = 'none';
            }
        };
    }

    if (authSubmit) {
        authSubmit.onclick = (e) => {
            e.preventDefault();
            const email = emailInput ? emailInput.value.trim() : '';
            const name = nameInput ? nameInput.value.trim() : '';
            
            // Use entered name, or extract from email, or default
            let displayName = name || 'User';
            if (!name && email && email.includes('@')) {
                displayName = email.split('@')[0].replace(/[._]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
            }
            
            updateState({ user: { ...getState().user, name: displayName, email: email } });
            location.href = 'landing.html';
        };
    }
}

function goToProfile() {
    const state = getState();
    // Check if user is signed in by checking if email exists in state
    if (state.user && state.user.email) {
        location.href = 'profile.html';
    } else {
        location.href = 'auth.html';
    }
}

window.goToProfile = goToProfile;

window.REVO = {
    getState,
    saveState,
    updateState,
    formatCurrency
};
