document.addEventListener('DOMContentLoaded', () => {
    let draggedImg = null;

    // Toggle visibility of training tab and overlay
    const trainingButton = document.getElementById('TrainingButton');
    const tab = document.getElementById('trainTab');
    const overlay = document.getElementById('overlay');
    const deleteButton = document.getElementById('deleteSelectedImages');

    trainingButton.addEventListener('click', function(event) {
        if (tab.style.display === 'block') {
            tab.style.display = 'none';
            overlay.style.display = 'none';
            document.body.style.overflow = 'auto';
            if (deleteButton) deleteButton.style.display = 'block';
        } else {
            tab.style.display = 'block';
            overlay.style.display = 'block';
            document.body.style.overflow = 'hidden';
            if (deleteButton) deleteButton.style.display = 'none';
        }
        event.stopPropagation();
    });

    tab.addEventListener('click', function(event) {
        event.stopPropagation();
    });

    // Drag and drop within 'scrollableFrame' and '.dropZone'
    const scrollableFrame = document.getElementById('scrollableFrame');
    const imgs = scrollableFrame ? scrollableFrame.querySelectorAll('img') : [];
    imgs.forEach(img => attachDragEvents(img));

    document.querySelectorAll('.scrollable-frame img').forEach(img => attachDragEvents(img));
    document.querySelectorAll('.dropZone').forEach(dropZone => attachDropZoneEvents(dropZone));

    // Selecting and deleting images
    const displayResult = document.getElementById('DisplayResult');
    if (displayResult) {
        displayResult.addEventListener('click', (event) => {
            if (event.target.classList.contains('image')) {
                event.target.classList.toggle('selected');
            }
        });
    }

    if (deleteButton) {
        deleteButton.addEventListener('click', () => {
            const selectedImages = document.querySelectorAll('#DisplayResult .image.selected');
            const imageUrls = Array.from(selectedImages).map(img => img.getAttribute('src'));
            removeSelectedImages(selectedImages, imageUrls);
        });
    }

    // Starting training with selected images
    const startTrainingButton = document.getElementById('startTrainingButton');
    if (startTrainingButton) {
        startTrainingButton.addEventListener('click', startTraining);
    }
});

// Function to attach drag events to images
function attachDragEvents(img) {
    img.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', ''); // For Firefox
        e.dataTransfer.effectAllowed = 'move';
        draggedImg = img;
    }, false);

    img.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }, false);

    img.addEventListener('drop', (e) => {
        e.preventDefault();
        handleImageDrop(e, img);
    }, false);
}

// Function to handle dropping images into new positions
function handleImageDrop(e, img) {
    if (e.target.tagName === 'IMG' && draggedImg !== e.target) {
        const targetRect = e.target.getBoundingClientRect();
        const targetCenter = targetRect.left + targetRect.width / 2;

        // Insert before the target image if the cursor is on the left half of it,
        // otherwise insert after the target image.
        const insertBefore = e.clientX < targetCenter;

        if (insertBefore) {
            e.target.parentNode.insertBefore(draggedImg, e.target);
        } else {
            e.target.parentNode.insertBefore(draggedImg, e.target.nextSibling);
        }
    }
}


// Function to attach events to drop zones
function attachDropZoneEvents(dropZone) {
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }, false);

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        if (draggedImg) {
            while (dropZone.firstChild) {
                dropZone.removeChild(dropZone.firstChild);
            }
            const clonedImg = draggedImg.cloneNode(true);
            adjustClonedImageStyles(clonedImg);
            dropZone.appendChild(clonedImg);
            draggedImg = null;
        }
    }, false);
}

// Function to adjust styles of cloned images
function adjustClonedImageStyles(clonedImg) {
    clonedImg.style.width = '100%';
    clonedImg.style.height = 'auto';
    clonedImg.style.borderRadius = 'inherit';
}

// Function to remove selected images
function removeSelectedImages(selectedImages, imageUrls) {
    fetch('/remove-images', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ urls: imageUrls }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        selectedImages.forEach(image => image.remove());
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Function to start training with selected images
function startTraining() {
    const dropZoneImages = document.querySelectorAll('.dropZone img');
    const imageNames = Array.from(dropZoneImages).map(img => img.getAttribute('name') || img.getAttribute('id'));

    fetch('/start-training', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageNames: imageNames }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
