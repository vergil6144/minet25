document.addEventListener('DOMContentLoaded', function() {
    mapOpen = document.getElementById('map-open');
    mapClose = document.getElementById('map-close');

    mapContainer = document.querySelector('.map-container');

    mapOpen.addEventListener('click', function() {
        mapContainer.style.display = 'flex';
    })

    mapClose.addEventListener('click', function() {
        mapContainer.style.display = 'none';
    })

    const mapHeader = document.querySelector('.map-header');
    
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    function dragStart(e) {
        if (e.type === "touchstart") {
            initialX = e.touches[0].clientX - xOffset;
            initialY = e.touches[0].clientY - yOffset;
        } else {
            initialX = e.clientX - xOffset;
            initialY = e.clientY - yOffset;
        }

        if (e.target === mapHeader || mapHeader.contains(e.target)) {
            isDragging = true;
            mapContainer.style.cursor = 'grabbing';
        }
    }

    function dragEnd() {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;
        mapContainer.style.cursor = 'move';
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            
            if (e.type === "touchmove") {
                currentX = e.touches[0].clientX - initialX;
                currentY = e.touches[0].clientY - initialY;
            } else {
                currentX = e.clientX - initialX;
                currentY = e.clientY - initialY;
            }

            xOffset = currentX;
            yOffset = currentY;

            mapContainer.style.transform = `translate(${currentX}px, ${currentY}px)`;
        }
    }

    // Mouse events
    mapContainer.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    // Touch events for mobile
    mapContainer.addEventListener('touchstart', dragStart);
    document.addEventListener('touchmove', drag);
    document.addEventListener('touchend', dragEnd);
})