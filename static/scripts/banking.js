document.addEventListener('DOMContentLoaded', async function() {
    transres = await fetch('/api/transaction?user_id=7665574291');
    console.log(transres)
    if (transres.ok) {
        const transactions = await transres.json();
        console.log(transactions);
        
        const transactionList = document.querySelector('.transaction-list');
        if (transactionList) {
            transactions.forEach(transaction => {
                item = document.createElement('div');
                item.className = 'transaction-item';
                date = document.createElement('span')
                date.className = 'transaction-date';
                date.textContent = transaction.date;

                desc = document.createElement('span')
                desc.className = 'transaction-description';
                desc.textContent = (transaction.desc).substring(0, 10) + '...';

                target = document.createElement('span')
                target.className = 'transaction-target';
                target.textContent = transaction.target;

                amount = document.createElement('span')
                amount.className = 'transaction-amount';
                if (transaction.Type === "credit") {
                    amount.textContent = `+${transaction.amount}`;
                    amount.classList.add('credit');
                }
                else {
                    amount.textContent = `-${transaction.amount}`;
                    amount.classList.add('debit');
                }

                item.appendChild(date);
                item.appendChild(desc);
                item.appendChild(target);
                item.appendChild(amount);

                transactionList.appendChild(item);



            });
        }
    }
})
