document.addEventListener('DOMContentLoaded', async function() {
    userData = await authFunc();
     console.log(userData);
    userId = userData.device_id;
    transres = await fetch(`/api/transactions/all?user_id=${userId}`);
    balance = document.querySelector('.balance-amount');
    if (balance) {
        balance.textContent = "$"+ userData.balance;
    }
    if (transres.ok) {
        const transactions = await transres.json();
        console.log(transactions);
        
        const transactionList = document.querySelector('.transaction-list');
        if (transactionList) {
            transactions.forEach(transaction => {
                item = document.createElement('div');
                item.className = 'transaction-item';
                item.id = transaction.id;
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
                    amount.textContent = `${transaction.amount}`;
                    amount.classList.add('credit');
                }
                else {
                    amount.textContent = `${transaction.amount}`;
                    amount.classList.add('debit');
                }

                item.appendChild(date);
                item.appendChild(desc);
                item.appendChild(target);
                item.appendChild(amount);
                item.addEventListener('click',openWindow)
                transactionList.appendChild(item);



            });
        }
    }
})

const openWindow = async (e)=>{
     var amendmentWindow = document.querySelector('.transaction-window');

     console.log(e.currentTarget);
     transactionID = e.currentTarget.id;

     transaction = await fetch(`/api/transaction?transaction_id=${transactionID}&user_id=7665574291`);

    if (transaction.ok) {
        transaction = await transaction.json()
        console.log(transaction);

        targetVal = document.querySelector('.target-value');
        targetVal.textContent = transaction.target;

        amountVal = document.querySelector('.amount-value');
        amountVal.textContent = transaction.amount;

        idVal = document.querySelector('.id-value');
        idVal.textContent = transaction.id;

        dateVal = document.querySelector('.date-value');
        dateVal.textContent = transaction.date;

        descVal = document.querySelector('.description-value');
        descVal.textContent = transaction.description;

        if (transaction.Type === "credit") {
            typeVal = document.querySelector('.type-value');
            typeVal.textContent = "Credit";
            typeVal.classList.add('credit');
            typeVal.classList.remove('debit');
        }else{
            typeVal = document.querySelector('.type-value');
            typeVal.textContent = "Debit";
            typeVal.classList.add('debit');
            typeVal.classList.remove('credit');
        }
    }

     if (amendmentWindow) {
                amendmentWindow.style.display = 'block';
                amendmentWindow.style.left = '50%';
                amendmentWindow.style.top = '50%';
                amendmentWindow.style.transform = 'translate(-50%, -50%)';
            }
}