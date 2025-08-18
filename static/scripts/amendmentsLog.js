document.addEventListener('DOMContentLoaded', async function() {
    const amendLog = document.querySelector('.amendment-log');
    amendment = await fetchAmendments();
    console.log(amendment);
    amendment.forEach(amm => {
        console.log(amm);
        item = document.createElement('div');
        item.className = 'amendment-item';
        title = document.createElement('p');
        title.className = 'Title';
        title.textContent = amm.title;
        description = document.createElement('p');
        description.className = 'Description';
        description.textContent = amm.amendment_disc.substring(0, 20) + '...';
        date = document.createElement('p');
        date.className = 'Date';
        date.textContent = amm.date_proposed
        item.appendChild(title);
        item.appendChild(description);
        item.appendChild(date);
        amendLog.appendChild(item);
    })


})

const fetchAmendments = async () => {
    try {
        const response = await fetch('/api/ammendments/all');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const amendments = await response.json();
        return amendments;
    } catch (error) {
        console.error('Error fetching amendments:', error);
        return [];
    }
}