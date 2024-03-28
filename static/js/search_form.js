document.addEventListener('DOMContentLoaded', (event) => {
    var tab = document.getElementById('trainTab');
    var overlay = document.getElementById('overlay');
    var deleteButton = document.getElementById('deleteSelectedImages'); // Get the delete button
    let draggedImg = null;

    // Functionality for TrainingButton click event
    function handleTrainingButtonClick(event) {
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
    }

    // TrainTab click event to stop propagation
    tab.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent the tab click from bubbling to the document, which would hide it
    });

    // TrainingButton click events
    const trainingButtons = document.querySelectorAll('#TrainingButton');
    trainingButtons.forEach(button => {
        button.addEventListener('click', handleTrainingButtonClick);
    });

    // Image drag and drop functionality
    const scrollableFrame = document.getElementById('scrollableFrame');
    const imgs = document.querySelectorAll('.scrollable-frame img, .dropZone img');

    imgs.forEach(img => {
        img.addEventListener('dragstart', (e) => {
            draggedImg = img; // Store the reference to the dragged image
            e.dataTransfer.setData('text/plain', ''); // Necessary for Firefox
            e.dataTransfer.effectAllowed = 'move';
        }, false);

        img.addEventListener('dragover', (e) => {
            e.preventDefault(); // Necessary to allow dropping
            e.dataTransfer.dropEffect = 'move';
        }, false);

        img.addEventListener('drop', (e) => {
            e.preventDefault(); // Prevent default action
            handleImageDrop(e, img, scrollableFrame, draggedImg);
        }, false);
    });

    // Drop zone functionality
    const dropZones = document.querySelectorAll('.dropZone');
    dropZones.forEach(dropZone => {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault(); // Allow the drop
            e.dataTransfer.dropEffect = 'move';
        }, false);

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            handleDropZoneDrop(e, dropZone, draggedImg);
        }, false);
    });

    // Handling clicks on DisplayResult for toggling selected class on images
    const displayResult = document.getElementById('DisplayResult');
    displayResult.addEventListener('click', (event) => {
        if (event.target.classList.contains('image')) {
            event.target.classList.toggle('selected');
        }
    });

    // Delete selected images functionality
    if (deleteButton) {
        deleteButton.addEventListener('click', handleDeleteSelectedImages);
    }

    // Start training button functionality
    const startTrainingButton = document.getElementById('startTrainingButton');
    if (startTrainingButton) {
        startTrainingButton.addEventListener('click', handleStartTraining);
    }
});

function handleImageDrop(e, img, scrollableFrame, draggedImg) {
    // Logic for reordering images or handling drops
}

function handleDropZoneDrop(e, dropZone, draggedImg) {
    // Logic for handling drop in drop zones
}

function handleDeleteSelectedImages() {
    // Logic for deleting selected images
}

function handleStartTraining() {
    // Logic for starting the training process
}
