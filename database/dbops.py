from database.db import db_manager 
import qrcode
from pyzbar import pyzbar
import cv2
import numpy as np
import io
import os
from PIL import Image
from datetime import datetime
import logging,random

def gen_str(length=60):
    """Generate a random string of fixed length"""
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def get_user_by_token(token):
    """Get user by token"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            print(token)
            cursor = await conn.execute("SELECT username,device_id,email,age,gender FROM users WHERE token = ?", (token,))
            user = await cursor.fetchone()
            return user
        finally:
            await conn.close()
            
    except Exception as e:
        print(e)
        logging.error(f"Error fetching user by token: {e}")
        raise
async def get_user_by_id(id):
    """Get user by token"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            cursor = await conn.execute("SELECT * FROM users WHERE device_id = ?", (int(id),))
            user = await cursor.fetchone()
            return dict(user) if user else None
        finally:
            await conn.close()
            
    except Exception as e:
        print(e)
        logging.error(f"Error fetching user by token: {e}")
        raise
def get_id():
    min_value = 10**(10-1)
    max_value = 10**10 - 1
    
    return random.randint(min_value, max_value)


async def create_user(username,email,gender,age,password_hash):
    """Create a new user in the database"""
    
    try:
        device_id = get_id()
        print(device_id)
        qr_path = generate_user_qr(device_id, username)
        conn = await db_manager.get_connection()
        token = gen_str(60)
        
        try:
            await conn.execute(
                """INSERT INTO users (username,token,email,device_id,age,gender, password_hash,qr_path)
                   VALUES (?, ?, ?, ?, ?, ?,?,?)""",(username,token, email, get_id(),age,gender,password_hash,qr_path))
            await conn.commit()
        finally:
            await conn.close()
    except Exception as e:
        print(e)
        logging.error(f"Error creating user: {e}")
        raise

async def get_all_users():
    """Get all users from the database"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            cursor = await conn.execute("SELECT * FROM users")
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        raise


def generate_user_qr(user_id, username):
    """Generate a QR code for the user"""
    try:
        qr_data = f"{user_id}:{username}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_path = f"qr_codes/{user_id}.png"
        img.save(img_path)
        
        return img_path
    except Exception as e:
        logging.error(f"Error generating QR code: {e}")

async def parse_user_qr(img_content):
    try:
        pil_image = Image.open(io.BytesIO(img_content))
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        decoded_objects = pyzbar.decode(cv_image)

        if  decoded_objects:

            qr_data = decoded_objects[0].data.decode('utf-8')

            if ':' in qr_data:
                device_id, username = qr_data.split(':', 1)
                user = await verify_user_qr(device_id, username)
                if user:
                    return {
                        'success': True,
                        'device_id': device_id,
                        'username': username,
                        'raw_data': qr_data 
                    }
                else:
                    return {
                        'success':False
                    }
            else:
                return {
                    'success':False
                }
        else:
            raise ValueError("No QR code found in the image")
    except Exception as e:
        logging.error(f"Error parsing QR code: {e}")
        print(e)
        return {
            'success': False,
            'error': str(e)
        }
    
async def verify_user_qr(device_id,username):
    """Verify if the user exists in the database using QR code data"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            cursor = await conn.execute(
                "SELECT * FROM users WHERE device_id = ? AND username = ?",
                (device_id, username)
            )
            user = await cursor.fetchone()
            return user is not None
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error verifying user QR: {e}")
        raise

async def get_all_ammendments():
    """Get all amendments from database"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            cursor = await conn.execute("SELECT * FROM amendments ORDER BY date_proposed")
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            # Always close the connection
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error fetching amendments: {e}")
        raise

async def create_amendment(title, description, number, date_proposed):
    """Create new amendment"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            await conn.execute(
                """INSERT INTO amendments (title, amendment_disc, date_proposed)
                   VALUES (?, ?, ?)""",
                (title, description, date_proposed)
            )
            await conn.commit()
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error creating amendment: {e}")
        raise

async def get_all_documents_for_user(user_id):
    """Get all documents from database"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            cursor = await conn.execute("SELECT * FROM documents WHERE user_id = ?", (user_id,))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        raise

async def verify_login(username, password_hash):
    """Verify user login credentials"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            cursor = await conn.execute(
                "SELECT * FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            user = await cursor.fetchone()
            if user:
                return user["token"]
            else:
                return None
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error verifying login: {e}")
        raise

async def upload_document(user_id, filename, mime_type, file_path):
    """Upload a document to the database"""
   
    try:
        conn = await db_manager.get_connection()
        
        try:
            await conn.execute(
                """INSERT INTO documents (user_id, document_name, mime_type, file_path)
                   VALUES (?, ?, ?, ?)""",
                (user_id, filename, mime_type, file_path)
            )

            await conn.commit()
        finally:
            await conn.close()
            
    except Exception as e:

        logging.error(f"Error uploading document: {e}")
        raise

async def attemptTransaction(reciever_id,sender_id,amount,Type):
    """Attempt a transaction between two users"""
    try:
        conn = await db_manager.get_connection()
        
        try:

            sender = await get_user_by_id(sender_id)
            reciever = await get_user_by_id(reciever_id)

            if not sender or not reciever:
                logging.error("Sender or receiver not found")
                raise ValueError("Sender or receiver not found")

            if sender['balance'] < amount:
                logging.error("Insufficient balance for transaction")
                raise ValueError("Insufficient balance for transaction")
            
            await update_user_balance(sender_id, -amount)
            await update_user_balance(reciever_id, amount)

            transaction_date = datetime.now().isoformat()
            await conn.execute(
                """INSERT INTO transactions (receiver_id, sender_id, amount, transaction_type,date)
                   VALUES (?, ?, ?, ?,?)""",
                (reciever_id, sender_id, amount, Type, transaction_date)
            )
            await conn.commit()
            return True
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error attempting transaction: {e}")
        print(e)
        raise

async def update_user_balance(user_id, amount):
    """Update user balance"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            await conn.execute(
                "UPDATE users SET balance = balance + ? WHERE device_id = ?",
                (amount, user_id)
            )
            await conn.commit()
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error updating user balance: {e}")
        raise

async def get_transactions_by_user(user_id):
    """Get all transactions for a user"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            cursor = await conn.execute(
                """SELECT id, transaction_type, amount, 
                   DATE(date) as date, sender_id, receiver_id 
                   FROM transactions 
                   WHERE sender_id = ? OR receiver_id = ?
                   ORDER BY date DESC""",
                (user_id, user_id)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error fetching transactions: {e}")
        raise

async def get_transaction_by_id(transaction_id):
    """Get a specific transaction by ID"""
    try:
        conn = await db_manager.get_connection()
        
        try:
            cursor = await conn.execute(
                "SELECT * FROM transactions WHERE id = ?",
                (transaction_id,)
            )
            transaction = await cursor.fetchone()
            return dict(transaction) if transaction else None
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error fetching transaction by ID: {e}")
        raise