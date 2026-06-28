from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StructuredRecord(BaseModel):
    id: str
    filename: str
    type: str
    title: str
    summary: str
    entities: list[str]
    keywords: list[str]
    priority: str
    confidence: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentOut(StructuredRecord):
    status: str
    created_at: datetime
    processed_at: datetime | None = None
    processing_time_ms: int | None = None


class UploadOut(BaseModel):
    id: str
    filename: str
    type: str
    status: str


class AnalyticsOut(BaseModel):
    total_files: int
    documents: int
    images: int
    audio: int
    average_processing_time_ms: float
    latest_uploads: list[DocumentOut]
    by_type: dict[str, int]
    by_priority: dict[str, int]


class SearchQuery(BaseModel):
    keyword: str | None = None
    entity: str | None = None
    title: str | None = None
    category: str | None = None
    date: str | None = None


class HealthOut(BaseModel):
    status: str
    offline_first: bool
    cpu_only: bool
    model_config = ConfigDict(protected_namespaces=())
    model_status: dict[str, str]
