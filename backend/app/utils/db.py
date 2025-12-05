from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["timetable"]

subjects_collection = db["subjects"]
teachers_collection = db["teachers"]
availability_collection = db["availability"]