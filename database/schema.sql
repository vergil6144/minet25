CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) UNIQUE NOT NULL,
    device_id INTEGER PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    qr_path VARCHAR(200),
    password_hash VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 10000.00
);

CREATE TABLE IF NOT EXISTS amendments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    amendment_disc VARCHAR(500) NOT NULL,
    date_proposed DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS queries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_subject VARCHAR(200) NOT NULL,
    query_content VARCHAR(500) NOT NULL,
    user_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_name VARCHAR(200) NOT NULL,
    mime_type VARCHAR(100),
    file_path VARCHAR(500) NOT NULL,
    user_id INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users(device_id),
    FOREIGN KEY (receiver_id) REFERENCES users(device_id)
);
CREATE TABLE IF NOT EXISTS stock_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(10) NOT NULL,      
    price DECIMAL(10, 2) NOT NULL,
    shares INTEGER NOT NULL
);

