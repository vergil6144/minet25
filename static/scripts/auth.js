const authFunc = async ()=>{
    token = localStorage.getItem('exminet_access_token');
       console.log(token)
    if (!token) {
        window.location.href = '/login';
        return;
    }
 

    const response = await fetch('/api/users/token-verify', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }});

    if (!response.ok) {
        console.error('Failed to verify token:', response.statusText);
        window.location.href = '/login';
        localStorage.removeItem('exminet_access_token');
        return;
    }

    userData = await response.json();
   
    return userData
}