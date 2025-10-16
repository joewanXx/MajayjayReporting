// --- Utility Functions ---

function formatUsernameAsEmail(username) {
    return `${username.toLowerCase().trim()}@brgyportal.io`;
}

function setButtonLoading(buttonId, isLoading, text = 'Loading...') {
    const button = document.getElementById(buttonId);
    if (!button) return;

    if (isLoading) {
        button.disabled = true;
        // You'll need to define the .loading-spinner class in your CSS for this to work visually
        button.innerHTML = `<div class="loading-spinner"></div> ${text}`;
    } else {
        button.disabled = false;
        if (buttonId === 'login-button') {
            button.innerHTML = 'Log In';
        } else if (buttonId === 'signup-button') {
            button.innerHTML = 'Sign Up';
        }
    }
}

function showToast(message, type = 'info') {
    // This function requires a #toast-container element in your HTML.
    const container = document.getElementById('toast-container');
    if (!container) {
        console.warn('Toast container not found. Message:', message);
        alert(message); // Fallback to alert
        return;
    }
    const toast = document.createElement('div');
    
    const colors = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        info: 'bg-blue-600',
        warning: 'bg-yellow-500'
    };
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        info: 'fa-info-circle',
        warning: 'fa-exclamation-triangle'
    }

    toast.innerHTML = `<i class="fas ${icons[type]} mr-2"></i> ${message}`;
    toast.className = `p-4 rounded-xl shadow-2xl text-white font-semibold z-50 ${colors[type]} transition-all duration-300 transform translate-x-full opacity-0 flex items-center`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.remove('translate-x-full', 'opacity-0');
    }, 10);

    setTimeout(() => {
        toast.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 4000); 
}

/**
 * Toggles the visibility of login and signup forms and updates tab styles.
 * @param {'login' | 'signup'} formType The type of form to show.
 */
function showAuthForm(formType) {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const loginTab = document.getElementById('login-tab');
    const signupTab = document.getElementById('signup-tab');

    if (formType === 'login') {
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
        loginTab.classList.add('border-green-600', 'text-green-600', 'bg-green-50');
        loginTab.classList.remove('border-gray-300', 'text-gray-500');
        signupTab.classList.add('border-gray-300', 'text-gray-500');
        signupTab.classList.remove('border-green-600', 'text-green-600', 'bg-green-50');
    } else {
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
        signupTab.classList.add('border-green-600', 'text-green-600', 'bg-green-50');
        signupTab.classList.remove('border-gray-300', 'text-gray-500');
        loginTab.classList.add('border-gray-300', 'text-gray-500');
        loginTab.classList.remove('border-green-600', 'text-green-600', 'bg-green-50');
    }
}

/**
 * Closes any modal by its ID.
 * @param {string} modalId The ID of the modal to close.
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if(modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

/**
 * Opens the admin management modal and populates it with data for a specific report.
 * @param {string} reportId The ID of the report to manage.
 */
function openAdminModal(reportId) {
    // The global mockReports variable must be populated in the HTML for this to work
    const report = mockReports.find(r => r.id === reportId);
    if (!report) {
        console.error("Report not found:", reportId);
        return;
    }

    // Populate modal fields with data from the found report
    document.getElementById('modal-report-title').textContent = report.title;
    document.getElementById('modal-report-id').textContent = report.id;
    document.getElementById('modal-report-reporter').textContent = report.reporter;
    document.getElementById('modal-report-location').textContent = report.location;
    document.getElementById('modal-report-description').textContent = report.description;
    document.getElementById('modal-current-report-id').value = report.id;
    document.getElementById('admin-status').value = report.status;
    document.getElementById('admin-response').value = report.response || '';
    document.getElementById('modal-current-proof').textContent = report.proof || 'None';

    // Show the modal
    const modal = document.getElementById('report-detail-modal');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}