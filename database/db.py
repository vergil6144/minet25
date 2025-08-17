import sqlite3
import aiosqlite
from pathlib import Path
import logging

DATABASE_PATH = Path(__file__).parent / "exminet.db"

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database with schema"""
        schema_path = Path(__file__).parent / "schema.sql"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON")
                
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_content = f.read()
                    statements = [s.strip() for s in schema_content.split(';') if s.strip()]
                    for statement in statements:
                        if statement:
                            conn.execute(statement)
                
                conn.commit()
                logging.info("Database initialized successfully")
                
        except sqlite3.OperationalError as e:
            logging.error(f"SQL syntax error in schema: {e}")
            raise
        except Exception as e:
            logging.error(f"Database initialization failed: {e}")
            raise
    
    async def get_connection(self):
        """Get a NEW asynchronous database connection each time"""
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        await conn.execute("PRAGMA foreign_keys = ON")
        return conn

# Global database manager instance
db_manager = DatabaseManager()