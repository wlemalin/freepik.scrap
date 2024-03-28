document.addEventListener('DOMContentLoaded', () => {
    // Add click event listeners to images within the scrollable frame
    initializeImageClickEvents();
});

function initializeImageClickEvents() {
    document.querySelectorAll('#scrollableFrame img').forEach(img => {
        img.addEventListener('click', handleImageClick);
    });
}

function handleImageClick() {
    const imageSrc = this.getAttribute('src'); // Get the 'src' attribute of the clicked image

    fetch('/album_dynamic_display', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({src: imageSrc}),
    })
    .then(response => response.json())
    .then(updateDisplayResult)
    .catch(error => console.error('Error:', error));
}

function updateDisplayResult(data) {
    const displayResult = document.getElementById('DisplayResult');
    displayResult.innerHTML = ''; // Clear the display area before showing new images

    // Append new images to the display area
    data.imageUrls.forEach(url => {
        let img = document.createElement('img');
        img.src = url;
        displayResult.appendChild(img);
    });
}
