from db import db_manager 

async def get_all_ammendments():
    async with await db_manager.get_connection() as conn:
        cursor = await conn.execute(
            "SELECT * FROM amendments ORDER BY date_proposed"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]