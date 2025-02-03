import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

class MongoConfig:

    def __init__(self, async_mode: bool = False):
        self.uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
        self.db_name = os.getenv('MONGO_DB_NAME', 'mydatabase')
        self.admin_password = os.getenv('MONGO_ADMIN_PASSWORD', 'default_password')

        self.async_mode = async_mode
        self.client = None
        self.async_client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            if self.async_mode:
                self.async_client = AsyncIOMotorClient(self.uri)
                self.db = self.async_client[self.db_name]
            else:
                self.client = MongoClient(self.uri)
                self.db = self.client[self.db_name]
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")

    def close(self):
        try:
            if self.async_mode and self.async_client:
                self.async_client.close()
            elif self.client:
                self.client.close()
            print("MongoDB connection closed")
        except Exception as e:
            print(f"Failed to close MongoDB connection: {e}")

    def check_connection(self):
        try:
            if self.async_mode:
                server_info = self.async_client.server_info()
            else:
                server_info = self.client.server_info()
            return "UP" if server_info.get("ok") == 1 else "DOWN"
        except Exception as e:
            return str(e)

