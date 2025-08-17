from database.db import db_manager 

import logging

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
                """INSERT INTO amendments (title, description, number, date_proposed)
                   VALUES (?, ?, ?, ?)""",
                (title, description, number, date_proposed)
            )
            await conn.commit()
        finally:
            await conn.close()
            
    except Exception as e:
        logging.error(f"Error creating amendment: {e}")
        raise