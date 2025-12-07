from app.utils.db import classes_collection

def fetch_classes():
    classes = list(classes_collection.find({}, {"_id": 0}))
    return classes