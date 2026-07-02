# LocalIntel AI

## Offline Multi-Modal Intelligence Platform

### Live Demo
🚀 **Access the Live Web App:** [localintel-ai-production-e07d.up.railway.app/upload](https://localintel-ai-production-e07d.up.railway.app/upload)

---

## Problem Statement

Organizations such as hospitals, government offices, legal firms, disaster response teams, and businesses receive large volumes of unstructured information including PDFs, scanned documents, images, audio recordings, and text files.

Processing this data manually is slow, error-prone, and often depends on cloud-based AI services. In many situations such as disaster zones, secure environments, or remote areas, internet connectivity is unavailable or restricted.

---

## Solution

LocalIntel AI is an offline-first, CPU-powered AI platform that converts unstructured data into structured JSON records.

The application processes:

- PDF documents
- Images
- Scanned documents
- Audio recordings
- Text files

All AI inference runs locally using CPU-only models without requiring cloud services.

---

## Features

- Offline AI processing
- CPU-only inference
- OCR for images
- Speech-to-text
- PDF & DOCX parsing
- Structured JSON generation
- SQLite database
- Search and filtering
- Export JSON & CSV
- Responsive web interface

---

## Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS

### Backend

- FastAPI
- SQLAlchemy

### Database

- SQLite

### AI Models

- llama.cpp
- Whisper.cpp
- PaddleOCR
- ONNX Runtime

---

## Architecture

User

↓

Upload File

↓

OCR / Speech / Parser

↓

Local AI Models

↓

Structured JSON

↓

SQLite Database

↓

Dashboard & Search

---

## Expected Outcome

A fully offline AI application capable of transforming unstructured files into structured datasets while maintaining user privacy and requiring only CPU resources.

---

## Team Members

| Member | Role |
|---------|------|
| Member 1 | Frontend & UI |
| Member 2 | Backend, AI & DevOps |

---

## License

GPL-3.0