# Installation Guide

## Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker compose up --build
```

The API runs on `http://localhost:8000` and the UI runs on `http://localhost:5173`.
