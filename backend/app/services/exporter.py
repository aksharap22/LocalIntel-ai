import csv
import json
from io import StringIO

from sqlalchemy.orm import Session, joinedload

from app.models.records import FileRecord
from app.services.processor import structured_from_models


def list_structured_records(db: Session) -> list[dict]:
    files = (
        db.query(FileRecord)
        .options(joinedload(FileRecord.processed_data))
        .filter(FileRecord.processed_data != None)  # noqa: E711
        .order_by(FileRecord.created_at.desc())
        .all()
    )
    return [
        structured_from_models(file, file.processed_data).model_dump(mode="json")
        for file in files
        if file.processed_data
    ]


def export_json(db: Session) -> str:
    return json.dumps(list_structured_records(db), indent=2)


def export_csv(db: Session) -> str:
    output = StringIO()
    rows = list_structured_records(db)
    fieldnames = [
        "id",
        "filename",
        "type",
        "title",
        "summary",
        "entities",
        "keywords",
        "priority",
        "confidence",
        "created_at",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        row["entities"] = "; ".join(row.get("entities", []))
        row["keywords"] = "; ".join(row.get("keywords", []))
        writer.writerow(row)
    return output.getvalue()
