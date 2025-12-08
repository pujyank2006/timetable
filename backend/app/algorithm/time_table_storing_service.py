from typing import Any, Dict

from app.utils.db import time_table_collection

def store_time_table(timetable_dict: Dict[str, Any]) -> Dict[str, Any]:
    summary = {"updated": [], "upserted": [], "errors": {}}

    for class_id, table in timetable_dict.items():
        try:
            doc = {"class_id": class_id, "ttable": table}
            res = time_table_collection.replace_one({"class_id": class_id}, doc, upsert=True)

            if getattr(res, "matched_count", 0):
                summary["updated"].append(class_id)
            else:
                summary["upserted"].append(class_id)

        except Exception as ex:
            summary["errors"][class_id] = str(ex)

    return summary