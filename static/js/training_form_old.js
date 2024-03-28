document.getElementById('trainTab').addEventListener('click', function(event) {
    event.stopPropagation();
});


document.addEventListener('DOMContentLoaded', (event) => {
    let draggedImg = null;

    const scrollableFrame = document.getElementById('scrollableFrame');
    const imgs = scrollableFrame.querySelectorAll('img');

    imgs.forEach(img => {
        img.addEventListener('dragstart', (e) => {
            draggedImg = img; // Store the dragged image
            e.dataTransfer.effectAllowed = 'move';
        }, false);

        img.addEventListener('dragover', (e) => {
            e.preventDefault(); // Necessary to allow dropping
            e.dataTransfer.dropEffect = 'move';
        }, false);

        img.addEventListener('drop', (e) => {
            e.preventDefault(); // Prevent default action
            if (e.target.tagName === 'IMG' && draggedImg !== e.target) {
                // Determine the drop location and move the draggedImg to that location
                const targetIndex = Array.from(scrollableFrame.children).indexOf(e.target);
                const draggedIndex = Array.from(scrollableFrame.children).indexOf(draggedImg);

                if (targetIndex < draggedIndex) {
                    e.target.parentNode.insertBefore(draggedImg, e.target);
                } else {
                    e.target.parentNode.insertBefore(draggedImg, e.target.nextSibling);
                }
            }
        }, false);
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    let draggedImg = null;

    // Attach dragstart event to images
    document.querySelectorAll('.scrollable-frame img').forEach(img => {
        img.addEventListener('dragstart', (e) => {
            draggedImg = img; // Store the reference to the dragged image
            e.dataTransfer.setData('text/plain', ''); // Necessary for Firefox
        }, false);
    });

    // Attach dragover and drop events to all drop zones
    document.querySelectorAll('.dropZone').forEach(dropZone => {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault(); // Allow the drop
            e.dataTransfer.dropEffect = 'move';
        }, false);

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            if (draggedImg) {
                // Clear existing images in the drop zone
                while (dropZone.firstChild) {
                    dropZone.removeChild(dropZone.firstChild);
                }

                // Clone the dragged image to keep the original intact
                const clonedImg = draggedImg.cloneNode(true); 
                clonedImg.style.width = '100%'; // Image fills the drop zone width
                clonedImg.style.height = 'auto'; // Maintain aspect ratio
                clonedImg.style.borderRadius = 'inherit'
                dropZone.appendChild(clonedImg); // Append the cloned image to the drop zone

                draggedImg = null; // Optional: Reset reference
            }
        }, false);
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const startTrainingButton = document.getElementById('startTrainingButton');

    if (startTrainingButton) {
        startTrainingButton.addEventListener('click', () => {
            // Select all images within the dropZone container(s)
            const dropZoneImages = document.querySelectorAll('.dropZone img');

            // Create an array of the image names or IDs
            // Assuming you want to fetch the 'name' or 'id' attribute of the images
            // Adjust according to what uniquely identifies your images for training
            const imageNames = Array.from(dropZoneImages).map(img => img.getAttribute('name') || img.getAttribute('id'));

            // Send the array to the server for starting the training process
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
                // Optionally, update the UI based on the response, like showing training status
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    }
});
