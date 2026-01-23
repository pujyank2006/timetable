from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["timetable"]

classes_collection = db["classes"]
teachers_collection = db["teachers"]
availability_collection = db["availability"]
time_table_collection = db["time_table"]
input_data_collection = db["input_data"]
invigilator_collection = db["invigilator"]