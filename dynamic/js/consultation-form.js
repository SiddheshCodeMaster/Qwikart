document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('consultation-form');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const data = {
            name: form.elements['name'].value,
            phone: form.elements['phone'].value,
            email: form.elements['email'].value
        };

        const response = await fetch('/submit-consultation', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        console.log('Response:', response);

        if (response.ok) {
            alert('Thank you for connecting with us, ' + data.name + '!');
            form.reset();
        } else {
            alert('There was an error. Please try again.');
        }
    });
});