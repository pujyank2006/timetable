import secrets
import yagmail
import os
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

def send_email(teacher_email, token):
    url = f"http://localhost:3000/teacher/availability?token={token}"

    body = f"""
    Hello Teacher, <br><br>
    Please use the following link to set your availability: <br>

    <a href="{url}" style = "
    background: #4CAF50;
    padding: 10px 16px;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    "> Open availability From </a> 

    <br><br>Or Click here: <br>
    {url}
    """

    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)
    yag.send(to = teacher_email, subject = "Submit availability", contents = body)