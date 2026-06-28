from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import Response
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.config import get_settings
from app.db.session import get_db
from app.models.records import FileRecord, HistoryRecord, ProcessedData
from app.schemas.records import AnalyticsOut, DocumentOut, HealthOut, UploadOut
from app.services.exporter import export_csv, export_json
from app.services.parser import SUPPORTED_EXTENSIONS, detect_file_type
from app.services.processor import process_file, structured_from_models

router = APIRouter()


@router.get("/health", response_model=HealthOut)
def health() -> HealthOut:
    settings = get_settings()
    return HealthOut(
        status="ok",
        offline_first=True,
        cpu_only=True,
        model_status={
            "llama.cpp": "configured" if settings.llama_model_path.exists() else "model_missing",
            "whisper.cpp": "configured"
            if settings.whisper_model_path.exists()
            else "model_missing",
            "paddleocr": "cpu_runtime",
            "onnxruntime": "cpu_runtime",
        },
    )


@router.post("/upload", response_model=UploadOut)
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)) -> UploadOut:
    settings = get_settings()
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds configured upload limit")

    file_id = str(uuid4())
    safe_name = Path(file.filename or f"{file_id}{suffix}").name
    destination = settings.upload_dir / f"{file_id}_{safe_name}"
    destination.write_bytes(content)
    file_type = detect_file_type(destination)
    record = FileRecord(
        id=file_id,
        filename=safe_name,
        content_type=file.content_type or "application/octet-stream",
        file_type=file_type,
        path=str(destination),
        size_bytes=len(content),
        status="uploaded",
    )
    db.add(record)
    db.add(HistoryRecord(file_id=file_id, event="uploaded", message=f"Uploaded {safe_name}"))
    db.commit()
    return UploadOut(id=file_id, filename=safe_name, type=file_type, status="uploaded")


@router.post("/process", response_model=DocumentOut)
def process(
    document_id: str = Query(..., alias="id"), db: Session = Depends(get_db)
) -> DocumentOut:
    file = db.get(FileRecord, document_id)
    if not file:
        raise HTTPException(status_code=404, detail="Document not found")
    return process_file(db, file)


@router.get("/documents", response_model=list[DocumentOut])
def documents(db: Session = Depends(get_db)) -> list[DocumentOut]:
    files = (
        db.query(FileRecord)
        .options(joinedload(FileRecord.processed_data))
        .order_by(FileRecord.created_at.desc())
        .all()
    )
    return [
        structured_from_models(file, file.processed_data)
        for file in files
        if file.processed_data is not None
    ]


@router.get("/document/{document_id}", response_model=DocumentOut)
def document(document_id: str, db: Session = Depends(get_db)) -> DocumentOut:
    file = db.get(FileRecord, document_id)
    if not file or not file.processed_data:
        raise HTTPException(status_code=404, detail="Document not found")
    return structured_from_models(file, file.processed_data)


@router.get("/search", response_model=list[DocumentOut])
def search(
    keyword: str | None = None,
    entity: str | None = None,
    title: str | None = None,
    category: str | None = None,
    date: str | None = None,
    db: Session = Depends(get_db),
) -> list[DocumentOut]:
    query = (
        db.query(FileRecord)
        .options(joinedload(FileRecord.processed_data))
        .join(FileRecord.processed_data)
    )
    if keyword:
        pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                ProcessedData.extracted_text.ilike(pattern),
                ProcessedData.summary.ilike(pattern),
                ProcessedData.title.ilike(pattern),
                FileRecord.filename.ilike(pattern),
            )
        )
    if title:
        query = query.filter(ProcessedData.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(FileRecord.file_type == category)
    if date:
        query = query.filter(FileRecord.created_at.cast(str).like(f"{date}%"))
    files = query.order_by(FileRecord.created_at.desc()).all()
    results = [
        structured_from_models(file, file.processed_data) for file in files if file.processed_data
    ]
    if entity:
        results = [item for item in results if entity.lower() in " ".join(item.entities).lower()]
    if keyword:
        results = [
            item
            for item in results
            if keyword.lower()
            in " ".join(
                [item.filename, item.title, item.summary, *item.keywords, *item.entities]
            ).lower()
        ]
    return results


@router.get("/analytics", response_model=AnalyticsOut)
def analytics(db: Session = Depends(get_db)) -> AnalyticsOut:
    files = db.query(FileRecord).options(joinedload(FileRecord.processed_data)).all()
    processed = [file for file in files if file.processed_data]
    by_type = {
        kind: sum(1 for file in files if file.file_type == kind)
        for kind in ["document", "image", "audio"]
    }
    priorities: dict[str, int] = {}
    for file in processed:
        priority = file.processed_data.priority if file.processed_data else "unknown"
        priorities[priority] = priorities.get(priority, 0) + 1
    times = [
        file.processing_time_ms or 0 for file in processed if file.processing_time_ms is not None
    ]
    latest = sorted(processed, key=lambda item: item.created_at, reverse=True)[:5]
    return AnalyticsOut(
        total_files=len(files),
        documents=by_type["document"],
        images=by_type["image"],
        audio=by_type["audio"],
        average_processing_time_ms=sum(times) / len(times) if times else 0,
        latest_uploads=[
            structured_from_models(file, file.processed_data)
            for file in latest
            if file.processed_data
        ],
        by_type=by_type,
        by_priority=priorities,
    )


@router.get("/export/json")
def download_json(db: Session = Depends(get_db)) -> Response:
    return Response(
        content=export_json(db),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=localintel-export.json"},
    )


@router.get("/export/csv")
def download_csv(db: Session = Depends(get_db)) -> Response:
    return Response(
        content=export_csv(db),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=localintel-export.csv"},
    )


@router.delete("/document/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    file = db.get(FileRecord, document_id)
    if not file:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(file)
    db.commit()
    return {"status": "deleted", "id": document_id}
