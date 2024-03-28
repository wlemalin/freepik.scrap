document.getElementById('TrainingButton').addEventListener('click', function(event) {
    var tab = document.getElementById('trainTab');
    var overlay = document.getElementById('overlay');
    var deleteButton = document.getElementById('deleteSelectedImages'); // Get the delete button
    
    // Toggle the display of the tab and overlay based on the current visibility of the tab
    if (tab.style.display === 'block') {
        tab.style.display = 'none'; // Hide the tab
        overlay.style.display = 'none'; // Hide the overlay
        document.body.style.overflow = 'auto'; // Re-enable scrolling on the body
        if (deleteButton) deleteButton.style.display = 'block'; // Show the delete button if trainTab is hidden
    } else {
        tab.style.display = 'block'; // Show the tab
        overlay.style.display = 'block'; // Show the overlay
        document.body.style.overflow = 'hidden'; // Disable scrolling on the body
        if (deleteButton) deleteButton.style.display = 'none'; // Hide the delete button if trainTab is displayed
    }
    event.stopPropagation(); // Prevent click event from propagating further
});

document.getElementById('trainTab').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent the tab click from bubbling to the document, which would hide it
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
document.getElementById('TrainingButton').addEventListener('click', function() {
    // Your code here. For example, navigate to a training page or open a modal
    // window.location.href = '/training-page-url'; // Example: Navigate to a training page
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

                // Optional: Adjust styles or classes of the cloned image if needed

                draggedImg = null; // Optional: Reset reference
            }
        }, false);
    });
});
document.addEventListener('DOMContentLoaded', () => {
    // Event delegation from the #DisplayResult container
    document.getElementById('DisplayResult').addEventListener('click', (event) => {
        console.log(event.target)
        // Check if the clicked element is an image with the 'image' class
        if (event.target.classList.contains('image')) {
            event.target.classList.toggle('selected');
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
const deleteButton = document.getElementById('deleteSelectedImages');

if (deleteButton) {
    deleteButton.addEventListener('click', () => {
        // Select all selected images within the DisplayResult container
        const selectedImages = document.querySelectorAll('#DisplayResult .image.selected');
        
        // Create an array of the selected image URLs
        const imageUrls = Array.from(selectedImages).map(img => img.getAttribute('src'));

        // Send the array to the server
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
            // Optionally, update the UI based on the response
        })
        .catch((error) => {
            console.error('Error:', error);
        });

        // Remove each selected image from the DOM
        selectedImages.forEach(image => {
            image.remove();
        });
    });
}
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
});