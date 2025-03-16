from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize MongoDB Connection
client = MongoClient(os.environ.get('MONGO_URI'))
db = client.get_database()  # Automatically uses the database in the URI

print("Database connection successful!")
