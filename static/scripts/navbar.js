

document.addEventListener('DOMContentLoaded', function() {
    navButtons = document.querySelectorAll('.nav-button');
    navButtons.forEach(function(button) {
        button.addEventListener('click', (e)=>{
            e.preventDefault();
            const target = e.target;
            const href = target.getAttribute('href');
            if (href) {
                if (window.location.pathname !== href) {
                    console.log(window.location.pathname)
                    window.location.href = href;
                }
            }
        })
    });
})