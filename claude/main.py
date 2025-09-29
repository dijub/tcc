from database_config import init_database, close_database

from models import Cliente
import asyncio 


asyncio.run(init_database())

asyncio.run(close_database())