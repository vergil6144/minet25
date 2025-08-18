document.addEventListener('DOMContentLoaded', function() {
    makeWindowMovable();
    scanBtn = document.querySelector('.scanner-container');
    imageInput = document.getElementById('image-input');
    
    scanBtn.addEventListener('click', function() {
        console.log("clicked")
        imageInput.click();
    })

    imageInput.addEventListener('change', async function(event) {
        const file = event.target.files[0];
        if (file){
            result = await processQRImage(file);
            if(result){
                loginWindow = document.querySelector('.auth-window');
                loginWindow.style.display = 'flex';
                username = document.querySelector('.username');
                console.log(result)
                username.textContent = result.username;
                submit = document.getElementById('login-button');

                submit.addEventListener('click', function() {
                    const password = document.getElementById('password').value;
                    if (password) {
                        const formData = new FormData();
                        formData.append('username', result.username);
                        formData.append('password', password);

                        fetch('/api/users/login', {
                            method: 'POST',
                            // Remove Content-Type header - browser sets it automatically for FormData
                            body: formData
                        }).then(response => response.json())
                          .then(data => {
                              if (data.status === 'success') {
                                  localStorage.setItem('exminet_access_token', data.token);
                                  alert(localStorage.getItem('exminet_access_token'));
                                  window.location.href = '/';
                              } else {
                                  alert('Login failed: ' + data.message);
                              }
                          })
                          .catch(error => {
                              console.error('Login error:', error);
                              alert('Login failed: ' + error.message);
                          });
                    } else {
                        alert('Please enter your password.');
                    }
                })

            }
        }
    })

    async function processQRImage(file){

        try{
            const formData = new FormData()
            formData.append('image',file)

            const response = await fetch("/api/users/verifyqr",{
                method: 'POST',
                body: formData
            })

            const result = await response.json();
            console.log(result)
            
            if (result.status == "success") {
                console.log("returning result")
                return result.user_data; 
                
            }
        }catch(error) {
            console.error('Error processing QR code:', error);
            statusIcon.src = '/static/images/icons/cross.png';
            return false; 
        }
    }
})

function makeWindowMovable() {
    const authWindow = document.querySelector('.auth-window');
    const authHeader = document.querySelector('.auth-header');
    const authClose = document.getElementById('auth-close');
    
    if (!authWindow || !authHeader) return;

    // State variables for dragging
    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let windowStartX = 0;
    let windowStartY = 0;

    function getWindowPosition() {
        const rect = authWindow.getBoundingClientRect();
        return { x: rect.left, y: rect.top };
    }

    function startDrag(e) {
        if (e.target === authClose) return; // Don't drag when clicking close button
        
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        
        const pos = getWindowPosition();
        windowStartX = pos.x;
        windowStartY = pos.y;
        
        authWindow.style.transition = 'none';
        authHeader.style.cursor = 'move';
        document.body.style.userSelect = 'none';
        e.preventDefault();
    }

    function drag(e) {
        if (!isDragging) return;
        
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        const newX = windowStartX + deltaX;
        const newY = windowStartY + deltaY;
        
        // Keep window within viewport bounds
        const maxX = window.innerWidth - authWindow.offsetWidth;
        const maxY = window.innerHeight - authWindow.offsetHeight;
        
        const boundedX = Math.max(0, Math.min(newX, maxX));
        const boundedY = Math.max(0, Math.min(newY, maxY));
        
        authWindow.style.left = boundedX + 'px';
        authWindow.style.top = boundedY + 'px';
        authWindow.style.transform = 'none';
    }

    function stopDrag() {
        if (!isDragging) return;
        
        isDragging = false;
        authHeader.style.cursor = 'move';
        document.body.style.userSelect = '';
        authWindow.style.transition = '';
    }

    function showWindow() {
        authWindow.style.display = 'block';
        authWindow.style.position = 'fixed';
        authWindow.style.left = '50%';
        authWindow.style.top = '50%';
        authWindow.style.transform = 'translate(-50%, -50%)';
        authWindow.style.zIndex = '1000';
    }

    function hideWindow() {
        authWindow.style.display = 'none';
        stopDrag(); // Stop dragging if window is closed while dragging
    }

    // Event listeners for dragging
    authHeader.addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', stopDrag);

    // Prevent text selection while dragging
    authHeader.addEventListener('selectstart', function(e) {
        e.preventDefault();
    });

    // Close button functionality
    if (authClose) {
        authClose.addEventListener('click', hideWindow);
    }

    // Double-click header to center window
    authHeader.addEventListener('dblclick', function() {
        authWindow.style.left = '50%';
        authWindow.style.top = '50%';
        authWindow.style.transform = 'translate(-50%, -50%)';
    });

    // Handle window resize to keep window in bounds
    window.addEventListener('resize', function() {
        if (authWindow.style.display === 'block') {
            const rect = authWindow.getBoundingClientRect();
            const maxX = window.innerWidth - authWindow.offsetWidth;
            const maxY = window.innerHeight - authWindow.offsetHeight;
            
            if (rect.left > maxX || rect.top > maxY) {
                const newX = Math.max(0, Math.min(rect.left, maxX));
                const newY = Math.max(0, Math.min(rect.top, maxY));
                
                authWindow.style.left = newX + 'px';
                authWindow.style.top = newY + 'px';
                authWindow.style.transform = 'none';
            }
        }
    });

    // Return control functions
    return {
        show: showWindow,
        hide: hideWindow
    };
}