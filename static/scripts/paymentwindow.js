document.addEventListener('DOMContentLoaded', function() {
    var paymentWindow = document.querySelector('.payment-window');
    const paymentHeader = document.querySelector('.payment-header');
    const paymentClose = document.querySelector('.payment-close');

    const items = document.querySelectorAll('.payment-item');
    console.log(items);
    items.forEach(item => {
        item.addEventListener('click', function() {
            // Show the payment window when a payment item is clicked
            if (paymentWindow) {
                paymentWindow.style.display = 'flex';
                paymentWindow.style.left = '50%';
                paymentWindow.style.top = '50%';
                paymentWindow.style.transform = 'translate(-50%, -50%)';
            }
        });
    })
    
    if (!paymentWindow || !paymentHeader) return;

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
            paymentWindow.appendChild(resizeDiv);
            
            resizeDiv.addEventListener('mousedown', startResize);
        });
    }

    // Get current window position
    function getWindowPosition() {
        const rect = paymentWindow.getBoundingClientRect();
        return {
            x: rect.left,
            y: rect.top
        };
    }

    // Start dragging
    function startDrag(e) {
        if (e.target === paymentClose || e.target.classList.contains('resize-')) return;
        
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        
        const pos = getWindowPosition();
        windowStartX = pos.x;
        windowStartY = pos.y;
        
        paymentWindow.style.transition = 'none';
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
        const maxX = window.innerWidth - paymentWindow.offsetWidth;
        const maxY = window.innerHeight - paymentWindow.offsetHeight;
        
        const boundedX = Math.max(0, Math.min(newX, maxX));
        const boundedY = Math.max(0, Math.min(newY, maxY));
        
        paymentWindow.style.left = boundedX + 'px';
        paymentWindow.style.top = boundedY + 'px';
        paymentWindow.style.transform = 'none';
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
        
        windowStartWidth = paymentWindow.offsetWidth;
        windowStartHeight = paymentWindow.offsetHeight;
        
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
        
        paymentWindow.style.width = newWidth + 'px';
        paymentWindow.style.height = newHeight + 'px';
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
        paymentWindow.style.display = 'block';
        paymentWindow.style.left = '50%';
        paymentWindow.style.top = '50%';
        paymentWindow.style.transform = 'translate(-50%, -50%)';
        paymentWindow.style.width = '500px';
        paymentWindow.style.height = 'auto';
    }

    // Hide window
    function hideWindow() {
        paymentWindow.style.display = 'none';
    }

    // Event listeners
    paymentHeader.addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    if (paymentClose) {
        paymentClose.addEventListener('click', hideWindow);
    }


    window.paymentWindow = {
        show: showWindow,
        hide: hideWindow
    };
});