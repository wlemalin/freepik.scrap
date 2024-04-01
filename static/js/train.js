document.addEventListener('DOMContentLoaded', () => {
    let draggedImg = null;

    // Stop propagation for clicks on 'trainTab'
    document.getElementById('trainTab').addEventListener('click', function(event) {
        event.stopPropagation();
    });

    // Handle image dragging within 'scrollableFrame'
    const scrollableFrame = document.getElementById('scrollableFrame');
    if (scrollableFrame) {
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
    }

    // Enhancements for dragging to '.dropZone'
    document.querySelectorAll('.scrollable-frame img').forEach(img => {
        img.addEventListener('dragstart', (e) => {
            draggedImg = img; // Store the reference to the dragged image
            e.dataTransfer.setData('text/plain', ''); // Necessary for Firefox
        }, false);
    });
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
                clonedImg.style.borderRadius = 'inherit';
                dropZone.appendChild(clonedImg); // Append the cloned image to the drop zone
    
                draggedImg = null; // Optional: Reset reference
            }
        }, false);
    });

    // Start training with selected images
    const startTrainingButton = document.getElementById('startTrainingButton');
    if (startTrainingButton) {
        startTrainingButton.addEventListener('click', () => {
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
                // Optionally, update the UI based on the response
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    }
});
