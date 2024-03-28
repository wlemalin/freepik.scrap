document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#scrollableFrame img').forEach(img => {
        img.addEventListener('click', function() {
            const imageSrc = this.getAttribute('src'); // Get the 'src' attribute of the clicked image

            fetch('/album_dynamic_display', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({src: imageSrc}),
            })
            .then(response => response.json())
            .then(data => {
                const displayResult = document.getElementById('DisplayResult');
                displayResult.innerHTML = ''; // Clear the display area before showing new images

                // Append new images to the display area
                data.imageUrls.forEach(url => {
                    let img = document.createElement('img');
                    img.src = url;
                    displayResult.appendChild(img);
                });
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
