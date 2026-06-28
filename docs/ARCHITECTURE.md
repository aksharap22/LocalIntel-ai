# Architecture

```mermaid
flowchart TD
    UI["React PWA"] --> API["FastAPI API"]
    API --> DB["SQLite"]
    API --> Parser["Document Parsers"]
    API --> OCR["OpenCV + PaddleOCR CPU"]
    API --> STT["whisper.cpp CPU"]
    Parser --> LLM["llama.cpp CPU"]
    OCR --> LLM
    STT --> LLM
    LLM --> JSON["Structured JSON"]
    JSON --> DB
    DB --> Export["JSON / CSV Export"]
```

## Backend Layers

- `api`: FastAPI routes
- `models`: SQLAlchemy tables
- `schemas`: Pydantic contracts
- `services`: parser, OCR, audio, local LLM, processor, exporter
- `core`: environment configuration

## Database Tables

- `files`
- `processed_data`
- `history`
- `settings`
