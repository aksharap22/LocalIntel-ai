# Project Specification

## Goal

LocalIntel AI converts unstructured local files into structured JSON without internet access or cloud AI APIs.

## Supported Inputs

- PDF
- DOCX
- PNG
- JPG
- JPEG
- WAV
- MP3
- TXT

## Structured Record

```json
{
  "id": "",
  "filename": "",
  "type": "",
  "title": "",
  "summary": "",
  "entities": [],
  "keywords": [],
  "priority": "",
  "confidence": "",
  "metadata": {}
}
```

## Non-Goals

- GPU acceleration
- Cloud inference
- Hosted model APIs
- Multi-user SaaS authentication
