FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LOCALINTEL_DATABASE_URL=sqlite:///./localintel.db

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
RUN mkdir -p /app/models /app/outputs

# Create a writable directory for the SQLite database and runtime artifacts.
# Railway's filesystem is writable inside the container, but the image only
# pre-creates the layout; the actual DB file is created by SQLAlchemy on
# first request. We seed an empty DB so health checks succeed out of the box.
RUN touch /app/localintel.db && chmod -R 0777 /app/outputs

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
