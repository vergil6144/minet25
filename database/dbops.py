from database.db import db_manager 
import qrcode
from pyzbar import pyzbar
import cv2
import numpy as np
import io
import os
from PIL import Image

import logging

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
            cursor = await conn.execute("SELECT username,device_id,email,age,gender FROM usersNew2 WHERE token = ?", (token,))
            user = await cursor.fetchone()
            return user
        finally:
            await conn.close()
            
    except Exception as e:
        print(e)
        logging.error(f"Error fetching user by token: {e}")
        raise

async def create_user(username,email,gender,age,device_id,password_hash):
    """Create a new user in the database"""
    
    try:
        qr_path = generate_user_qr(device_id, username)
        conn = await db_manager.get_connection()
        token = gen_str(60)
        
        try:
            await conn.execute(
                """INSERT INTO usersNew2 (username,token,email,device_id,age,gender, password_hash,qr_path)
                   VALUES (?, ?, ?, ?, ?, ?,?,?)""",(username,token, email, device_id,age,gender,password_hash,qr_path))
            await conn.commit()
        finally:
            await conn.close()
    except Exception as e:
        print(e)
        logging.error(f"Error creating user: {e}")
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
                "SELECT * FROM usersNew2 WHERE device_id = ? AND username = ?",
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
                "SELECT * FROM usersNew2 WHERE username = ? AND password_hash = ?",
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