from database_config import init_database, close_database
import asyncio 


asyncio.run(init_database())

asyncio.run(close_database())