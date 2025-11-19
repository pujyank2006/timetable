from app.utils.db import subjects_collection

def fetch_subjects():
    subjects = list(subjects_collection.find({}, {"_id": 0}))
    return subjects