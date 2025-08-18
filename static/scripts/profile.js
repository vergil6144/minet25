document.addEventListener('DOMContentLoaded', async function() {
    userData = JSON.parse(localStorage.getItem('exminet_user_data'));
    if (!userData) {
        window.location.href = '/login';
        return;
    }

    Name = document.getElementById('name');
    Email = document.getElementById('email');
    DeviceId = document.getElementById('device_id');
    Age = document.getElementById('age');
    Gender = document.getElementById('gender')
    
    Name.textContent = userData.username || 'N/A';
    Email.textContent = userData.email || 'N/A';
    DeviceId.textContent = userData.device_id || 'N/A';
    Age.textContent = userData.age
    Gender.textContent = userData.gender || 'N/A';
})