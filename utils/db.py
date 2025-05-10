"""This file contains the database functions"""
import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, future=True)

class Level(Base): # type: ignore   # pylint: disable=R0903
    """Model for the levels table"""
    __tablename__ = 'levels'

    guild_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, primary_key=True)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

class Punishments(Base): # type: ignore     # pylint: disable=R0903
    """Model for the punishments table"""
    __tablename__ = 'punishments'

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    user_id = Column(Integer)
    punishment_type = Column(String)
    punishment_time = Column(TIMESTAMP)
    punisher_id = Column(Integer)
    reason = Column(String)

async def init_db() -> None: # pylint: disable=W0718
    """Function to initialize the database"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Error creating tables: {e}")

async def get_user_data(guild_id: int, user_id: int) -> Level:
    """Function to get user data"""
    async with SessionLocal() as session:
        stmt = select(Level).filter(Level.guild_id == guild_id, Level.user_id == user_id)
        result = await session.execute(stmt)
        user_data = result.scalars().first()
        return user_data if user_data else Level(guild_id=guild_id, user_id=user_id)

async def update_user_data(guild_id: int, user_id: int, xp: int, level: int) -> None:
    """Function to update user data"""
    async with SessionLocal() as session:
        user_data = await get_user_data(guild_id, user_id)
        user_data.xp = xp
        user_data.level = level
        session.add(user_data)
        await session.commit()
