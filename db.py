import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variables
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/express')

client = MongoClient(MONGODB_URI)
db = client.express