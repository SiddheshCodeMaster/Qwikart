document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('consultation-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        // Example: Show a thank you message or send data via fetch/AJAX
        alert('Thank you for your order, ' + form.elements['name'].value + '!');
        form.reset();
    });
});