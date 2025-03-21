import functools
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

def handle_db_exceptions(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ServerSelectionTimeoutError as e:
            raise HTTPException(status_code=504, detail=f"MongoDB server selection timed out: {e}")
        except ConnectionFailure as e:
            raise HTTPException(status_code=503, detail=f"Could not connect to MongoDB: {e}")
    return wrapper