import asyncio
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash(password: str) -> str:
    return await asyncio.to_thread(pwd.hash, password)


async def verify(plain_password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(pwd.verify, plain_password, hashed_password)
