import sqlite3

conn = sqlite3.connect("exminet.db")
cur = conn.cursor()

cur.executescript("""
-- Users
INSERT INTO users (username, device_id, email, age, gender, qr_path, password_hash, token, balance)
VALUES
('alice', 1, 'alice@example.com', 28, 'Female', 'qr_codes/alice.png', 'hash_alice', 'token_alice', 9500.00),
('bob',   2, 'bob@example.com',   32, 'Male',   'qr_codes/bob.png',   'hash_bob',   'token_bob',   10500.00),
('charlie',3,'charlie@example.com',24,'Male',   'qr_codes/charlie.png','hash_charlie','token_charlie', 10000.00);

-- Amendments
INSERT INTO amendments (title, amendment_disc, date_proposed)
VALUES
('Free Trade Policy', 'Proposal to reduce tariffs on imports.', '2025-08-15'),
('Digital Privacy Act', 'Stronger regulations on user data protection.', '2025-08-18');

-- Queries
INSERT INTO queries (query_subject, query_content, user_id)
VALUES
('Login Issue', 'I cannot log into my account after password reset.', 1),
('Balance Discrepancy', 'My wallet balance seems incorrect.', 2);

-- Documents
INSERT INTO documents (document_name, mime_type, file_path, user_id)
VALUES
('contract_alice.pdf', 'application/pdf', 'docs/contract_alice.pdf', 1),
('id_bob.png',         'image/png',       'docs/id_bob.png',         2);

-- Transactions (money transfer between users)
INSERT INTO transactions (transaction_type, amount, date, sender_id, receiver_id)
VALUES
('TRANSFER', 500.00, '2025-08-19', 1, 2),  -- Alice sends Bob 500
('TRANSFER', 200.00, '2025-08-20', 2, 3); -- Bob sends Charlie 200

-- Stock Transactions (user trades with market)
INSERT INTO stock_transactions (stock_symbol, price_per_share)
VALUES
('AAPL', 150.25),
('TSLA', 720.50);

""")

conn.commit()
conn.close()

print("✅ Data seeded into exminet.db")
