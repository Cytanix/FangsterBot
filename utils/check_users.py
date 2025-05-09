"""This file checks how many users are in the database and returns it"""
import asyncio
from typing import Optional
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
load_dotenv()

# Async DB URL using asyncpg
DATABASE_URL = os.getenv('DATABASE_URL')

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)

async def check() -> Optional[int]:
    """The actual check function"""
    async with engine.connect() as conn:
        try:
            result = await conn.execute(text("SELECT COUNT(*) FROM levels"))
            count = result.scalar()
            print(count)
            return int(count)
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None

if __name__ == "__main__":
    asyncio.run(check())
