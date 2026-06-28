import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.records import FileRecord, HistoryRecord, ProcessedData
from app.schemas.records import DocumentOut
from app.services.audio import transcribe_audio
from app.services.llm import generate_metadata
from app.services.ocr import extract_image_text
from app.services.parser import detect_file_type, extract_document_text


def structured_from_models(file: FileRecord, data: ProcessedData) -> DocumentOut:
    return DocumentOut(
        id=file.id,
        filename=file.filename,
        type=file.file_type,
        title=data.title,
        summary=data.summary,
        entities=data.entities,
        keywords=data.keywords,
        priority=data.priority,
        confidence=data.confidence,
        metadata=data.metadata_json,
        status=file.status,
        created_at=file.created_at,
        processed_at=file.processed_at,
        processing_time_ms=file.processing_time_ms,
    )


def extract_text(path: Path, file_type: str) -> str:
    if file_type == "document":
        return extract_document_text(path)
    if file_type == "image":
        return extract_image_text(path)
    if file_type == "audio":
        return transcribe_audio(path)
    raise ValueError(f"Unsupported file type: {file_type}")


def process_file(db: Session, file: FileRecord) -> DocumentOut:
    started = time.perf_counter()
    path = Path(file.path)
    file_type = detect_file_type(path)
    text = extract_text(path, file_type)
    metadata = generate_metadata(text=text, filename=file.filename, file_type=file_type)
    settings = get_settings()
    elapsed_ms = int((time.perf_counter() - started) * 1000)

    data = file.processed_data or ProcessedData(id=str(uuid4()), file_id=file.id)
    data.title = str(metadata.get("title") or file.filename)
    data.summary = str(metadata.get("summary") or "")
    data.document_type = str(metadata.get("document_type") or file_type)
    data.entities = list(metadata.get("entities") or [])
    data.keywords = list(metadata.get("keywords") or [])
    data.priority = str(metadata.get("priority") or "medium")
    data.confidence = float(metadata.get("confidence") or 0)
    data.extracted_text = text
    source = "llama.cpp" if settings.llama_model_path.exists() else "deterministic-local-fallback"
    data.metadata_json = {
        "source": source,
        "text_length": len(text),
        "document_type": data.document_type,
    }

    file.file_type = file_type
    file.status = "processed"
    file.processed_at = datetime.utcnow()
    file.processing_time_ms = elapsed_ms
    db.add(data)
    db.add(
        HistoryRecord(
            file_id=file.id,
            event="processed",
            message=f"Processed in {elapsed_ms} ms",
        )
    )
    db.commit()
    db.refresh(file)
    db.refresh(data)
    return structured_from_models(file, data)
