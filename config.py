import os

class Config:
    API_ID = int(os.getenv("API_ID", "1234567"))
    API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")
    MONGO_URL = os.getenv("MONGO_URL", "YOUR_MONGO_URL")
    DB_NAME = os.getenv("DB_NAME", "RenameBotDB")
  
