document.addEventListener('DOMContentLoaded', function() {
    uploadButton = document.getElementById('upload');

    uploadButton.addEventListener('click', function() {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.onchange = async function(event) {
            const file = event.target.files[0];
            if (file) {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('title', file.name);
                formData.append('user_id', '1');
                try {
                    const response = await fetch('/api/documents/upload', {
                        method: 'POST',
                        body: formData
                    });
                    if (response.ok) {
                        alert('File uploaded successfully!');
                    } else {
                        alert('Failed to upload file.');
                    }
                } catch (error) {
                    console.error('Error uploading file:', error);
                }
            }
        };
        fileInput.click();
    })
})
document.addEventListener('DOMContentLoaded', async function() {
    openable = document.querySelectorAll('.openable');
    mapClose = document.getElementById('documents-close');

    docContainer = document.querySelector('.documents-window');

    openable.forEach(async function(item) {
        item.addEventListener('click',async function() {
            docContainer.style.display = 'flex';
            const docTitle = item.querySelector('.doc-tttle').textContent;
            docContainer.querySelector('.documents-title').textContent = docTitle;
            await populateDocWindow(item);
        });
       
    })

    async function populateDocWindow(item) {
        console.log(item)
        doc_id = item.getAttribute('id');
        if (true){
            documents = await fetch('/api/documents/all');
            content = document.querySelector('.documents-content');
            documents = await documents.json();
            content.innerHTML = '';

            documents.forEach(doc => {
             
                    const docItem = document.createElement('div');
                    docItem.className = 'file-item';
                    docItem.innerHTML = `
                        <img src="/static/images/icons/file.png" alt="Document Icon">
                        <div class="file-name">${doc.document_name}</div>
                    `;
                    console.log(doc)
                    content.appendChild(docItem);    
            })
        }else{
              content = document.querySelector('.documents-content');
            content.innerHTML = '';
        }
    }
    

    mapClose.addEventListener('click', function() {
        docContainer.style.display = 'none';
    })

    const docHeader = document.querySelector('.documents-header');
    
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

        if (e.target === docHeader || docHeader.contains(e.target)) {
            isDragging = true;
        }
    }

    function dragEnd() {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;
       
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

            docContainer.style.transform = `translate(${currentX}px, ${currentY}px)`;
        }
    }
    docContainer.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    docContainer.addEventListener('touchstart', dragStart);
    document.addEventListener('touchmove', drag);
    document.addEventListener('touchend', dragEnd);
})




