document.addEventListener('DOMContentLoaded', function() {
    const amendmentWindow = document.querySelector('.ammendment-window');
    const amendmentHeader = document.querySelector('.ammendment-header');
    const amendmentClose = document.querySelector('.ammendment-close');
    
    if (!amendmentWindow || !amendmentHeader) return;

    // Dragging variables
    let isDragging = false;
    let startX, startY;
    let windowStartX, windowStartY;

    // Resizing variables
    let isResizing = false;
    let resizeHandle = null;
    let windowStartWidth, windowStartHeight;

    // Create resize handles
    function createResizeHandles() {
        const handles = [
            { class: 'resize-se', cursor: 'se-resize' },
            { class: 'resize-s', cursor: 's-resize' },
            { class: 'resize-e', cursor: 'e-resize' }
        ];
        
        handles.forEach(handle => {
            const resizeDiv = document.createElement('div');
            resizeDiv.className = handle.class;
            resizeDiv.style.cursor = handle.cursor;
            amendmentWindow.appendChild(resizeDiv);
            
            resizeDiv.addEventListener('mousedown', startResize);
        });
    }

    // Get current window position
    function getWindowPosition() {
        const rect = amendmentWindow.getBoundingClientRect();
        return {
            x: rect.left,
            y: rect.top
        };
    }

    // Start dragging
    function startDrag(e) {
        if (e.target === amendmentClose || e.target.classList.contains('resize-')) return;
        
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        
        const pos = getWindowPosition();
        windowStartX = pos.x;
        windowStartY = pos.y;
        
        amendmentWindow.style.transition = 'none';
        document.body.style.userSelect = 'none';
        
        e.preventDefault();
    }

    // During drag
    function drag(e) {
        if (!isDragging) return;
        
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        const newX = windowStartX + deltaX;
        const newY = windowStartY + deltaY;
        
        // Keep within bounds
        const maxX = window.innerWidth - amendmentWindow.offsetWidth;
        const maxY = window.innerHeight - amendmentWindow.offsetHeight;
        
        const boundedX = Math.max(0, Math.min(newX, maxX));
        const boundedY = Math.max(0, Math.min(newY, maxY));
        
        amendmentWindow.style.left = boundedX + 'px';
        amendmentWindow.style.top = boundedY + 'px';
        amendmentWindow.style.transform = 'none';
    }

    // Stop dragging
    function stopDrag() {
        isDragging = false;
        document.body.style.userSelect = '';
    }

    // Start resizing
    function startResize(e) {
        isResizing = true;
        resizeHandle = e.target.className;
        startX = e.clientX;
        startY = e.clientY;
        
        windowStartWidth = amendmentWindow.offsetWidth;
        windowStartHeight = amendmentWindow.offsetHeight;
        
        document.body.style.userSelect = 'none';
        e.preventDefault();
        e.stopPropagation();
    }

    // During resize
    function resize(e) {
        if (!isResizing) return;
        
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        let newWidth = windowStartWidth;
        let newHeight = windowStartHeight;
        
        // Handle different resize directions
        if (resizeHandle.includes('resize-se')) {
            // Southeast corner - resize width and height
            newWidth = windowStartWidth + deltaX;
            newHeight = windowStartHeight + deltaY;
        } else if (resizeHandle.includes('resize-s')) {
            // South edge - resize height only
            newHeight = windowStartHeight + deltaY;
        } else if (resizeHandle.includes('resize-e')) {
            // East edge - resize width only
            newWidth = windowStartWidth + deltaX;
        }
        
        // Apply minimum and maximum constraints
        
        amendmentWindow.style.width = newWidth + 'px';
        amendmentWindow.style.height = newHeight + 'px';
    }

    // Stop resizing
    function stopResize() {
        isResizing = false;
        resizeHandle = null;
        document.body.style.userSelect = '';
    }

    // Handle mouse move for both drag and resize
    function handleMouseMove(e) {
        if (isDragging) {
            drag(e);
        } else if (isResizing) {
            resize(e);
        }
    }

    // Handle mouse up for both drag and resize
    function handleMouseUp() {
        if (isDragging) {
            stopDrag();
        }
        if (isResizing) {
            stopResize();
        }
    }

    // Show window
    function showWindow() {
        amendmentWindow.style.display = 'block';
        amendmentWindow.style.left = '50%';
        amendmentWindow.style.top = '50%';
        amendmentWindow.style.transform = 'translate(-50%, -50%)';
        amendmentWindow.style.width = '500px';
        amendmentWindow.style.height = 'auto';
    }

    // Hide window
    function hideWindow() {
        amendmentWindow.style.display = 'none';
    }

    // Event listeners
    amendmentHeader.addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    if (amendmentClose) {
        amendmentClose.addEventListener('click', hideWindow);
    }

    // Create resize handles
    createResizeHandles();

    // Expose functions
    window.amendmentWindow = {
        show: showWindow,
        hide: hideWindow
    };
});