document.addEventListener('DOMContentLoaded', () => {
    preventEventPropagationOnTrainTab();
    initializeDragAndDropForImages();
    initializeDragAndDropForDropZones();
    initializeStartTrainingButton();
});

function preventEventPropagationOnTrainTab() {
    document.getElementById('trainTab').addEventListener('click', function(event) {
        event.stopPropagation();
    });
}

function initializeDragAndDropForImages() {
    let draggedImg = null;
    const scrollableFrame = document.getElementById('scrollableFrame');
    const imgs = document.querySelectorAll('#scrollableFrame img, .scrollable-frame img');

    imgs.forEach(img => {
        img.addEventListener('dragstart', (e) => {
            draggedImg = img; // Store the dragged image
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', ''); // Necessary for Firefox
        }, false);

        img.addEventListener('dragover', (e) => {
            e.preventDefault(); // Necessary to allow dropping
            e.dataTransfer.dropEffect = 'move';
        }, false);

        img.addEventListener('drop', (e) => {
            e.preventDefault(); // Prevent default action
            if (e.target.tagName === 'IMG' && draggedImg !== e.target) {
                handleImageDrop(e, scrollableFrame, draggedImg);
            }
        }, false);
    });
}

function initializeDragAndDropForDropZones() {
    let draggedImg = null;

    document.querySelectorAll('.dropZone').forEach(dropZone => {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault(); // Allow the drop
            e.dataTransfer.dropEffect = 'move';
        }, false);

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            if (draggedImg) {
                handleDropZoneDrop(dropZone, draggedImg);
                draggedImg = null; // Reset reference after dropping
            }
        }, false);
    });
}

function initializeStartTrainingButton() {
    // Implementation remains unchanged
}

function handleImageDrop(e, scrollableFrame, draggedImg) {
    const targetIndex = Array.from(scrollableFrame.children).indexOf(e.target);
    const draggedIndex = Array.from(scrollableFrame.children).indexOf(draggedImg);

    if (targetIndex < draggedIndex) {
        e.target.parentNode.insertBefore(draggedImg, e.target);
    } else {
        e.target.parentNode.insertBefore(draggedImg, e.target.nextSibling);
    }
}

function handleDropZoneDrop(dropZone, draggedImg) {
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
}
