import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings
from app.db.session import Base, engine
from app.models import records  # noqa: F401

logger = logging.getLogger(__name__)


def _maybe_download_models() -> None:
    """Download AI model files if they are missing.

    This is the offline-first guarantee: on first run with no internet, the
    download fails and the app still starts, but the LLM/whisper services
    will fall back to deterministic extraction. Once models are present
    on disk, the app runs fully offline forever.
    """
    settings = get_settings()
    needs_llm = not settings.llama_model_path.exists()
    needs_whisper = not settings.whisper_model_path.exists()
    if not (needs_llm or needs_whisper):
        logger.info("Models present; skipping download.")
        return
    if os.getenv("LOCALINTEL_SKIP_MODEL_DOWNLOAD") == "1":
        logger.warning(
            "Models missing but LOCALINTEL_SKIP_MODEL_DOWNLOAD=1; "
            "skipping download. App will use deterministic fallback."
        )
        return

    # Resolve the download script relative to the repo root.
    # Repo layout: <repo>/scripts/download_models.py
    # In Docker: WORKDIR /app, scripts mounted at /app/scripts/...
    candidates = [
        Path("/app/scripts/download_models.py"),
        Path(__file__).resolve().parents[2] / "scripts" / "download_models.py",
        Path.cwd() / "scripts" / "download_models.py",
    ]
    script = next((p for p in candidates if p.exists()), None)
    if script is None:
        logger.warning("download_models.py not found; skipping download.")
        return

    import subprocess  # nosec B404

    logger.info("Some models missing; running download_models.py …")
    try:
        subprocess.run(  # nosec B603
            ["python", str(script)],
            check=True,
            timeout=1800,  # 30 min ceiling
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Model download failed (%s); continuing with fallback.", exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _maybe_download_models()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_origin_regex=settings.cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = create_app()
