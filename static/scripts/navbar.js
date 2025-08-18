const navMap = {
    "home": "/",
    "locker": "/locker",
    "profile": "/profile",
    "contact": "/contact",
    "ammendments": "/ammendments",
    "stocks": "/stocks",
}

document.addEventListener('DOMContentLoaded', function() {
    navButtons = document.querySelectorAll('.nav-button');
    navButtons.forEach(function(button) {
        button.addEventListener('click', (e)=>{
            e.preventDefault();
            active = document.querySelector('.nav-button.active');
            const dest = e.target.getAttribute('id');
            window.location.href = navMap[dest] || '/';
        })
    });

    navdropdowns = document.querySelectorAll('.nav-dropdown');
    navdropdowns.forEach(function(dropdown) {
        dropdown.addEventListener('click', (e)=>{
            e.preventDefault();
        })
    });

    dropdownItems = document.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(function(item) {
        item.addEventListener('click', (e)=>{
            e.preventDefault();
            const target = e.target;
            const dest = target.getAttribute('id');
            if (dest){
                window.location.href = navMap[dest] || '/';
            }
        })
    })
})