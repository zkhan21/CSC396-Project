import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv()

# Import Config (Fixing Import Path)
try:
    from backend.config import Config  # When running from project root
except ModuleNotFoundError:
    from config import Config  # When running from inside backend/

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client["SmartExpenseTracker"]

# Define Collections
expenses_collection = db["expenses"]
users_collection = db["users"]

print("✅ Connected to MongoDB Atlas")
