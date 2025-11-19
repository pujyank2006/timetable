import secrets

from app.utils.db import teachers_collection

def fetch_teachers():
    teachers = list(teachers_collection.find({}, {"_id": 0}))
    return teachers

def generate_token_for_teacher(teacher_id):
    token = secrets.token_hex(16)
    teachers_collection.update_one(
        {"id": teacher_id},
        {"$set": { "link_token": token }}
    )
    return token
