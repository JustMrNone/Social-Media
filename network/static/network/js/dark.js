document.addEventListener("DOMContentLoaded", function() {
    const darkModeToggle = document.getElementById('customSwitch1');

    // Check if dark mode is enabled in local storage
    const isDarkMode = localStorage.getItem('darkMode') === 'enabled';

    // Enable dark mode if it's already enabled
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }

    // Toggle dark mode
    darkModeToggle.addEventListener('change', () => {
        document.body.classList.toggle('dark-mode');
        if (darkModeToggle.checked) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', null);
        }
    });
});