document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-card form');
    const signupForm = document.querySelector('.signup-card form');
    const flashContainer = document.querySelector('.flash-container');

    function showMessage(message, type = 'success') {
        if (!flashContainer) return;

        flashContainer.innerHTML = '';

        const alertBox = document.createElement('div');
        alertBox.className = `flash ${type}`;
        alertBox.textContent = message;
        flashContainer.appendChild(alertBox);
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    loginForm?.addEventListener('submit', (event) => {
        event.preventDefault();

        const email = loginForm.querySelector('input[name="email"]').value.trim();
        const password = loginForm.querySelector('input[name="password"]').value.trim();

        if (!email || !password) {
            showMessage('Please fill in all login fields.', 'error');
            return;
        }

        if (!isValidEmail(email)) {
            showMessage('Please enter a valid email address.', 'error');
            return;
        }

        if (password.length < 6) {
            showMessage('Password must be at least 6 characters long.', 'error');
            return;
        }

        showMessage('Login successful!');
        loginForm.submit();
    });

    signupForm?.addEventListener('submit', (event) => {
        event.preventDefault();

        const name = signupForm.querySelector('input[name="name"]').value.trim();
        const email = signupForm.querySelector('input[name="email"]').value.trim();
        const password = signupForm.querySelector('input[name="password"]').value.trim();

        if (!name || !email || !password) {
            showMessage('Please fill in all signup fields.', 'error');
            return;
        }

        if (!isValidEmail(email)) {
            showMessage('Please enter a valid email address.', 'error');
            return;
        }

        if (password.length < 6) {
            showMessage('Password must be at least 6 characters long.', 'error');
            return;
        }

        showMessage('Account created successfully!');
        signupForm.submit();
    });
});
