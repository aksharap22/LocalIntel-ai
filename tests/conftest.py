import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

os.environ["LOCALINTEL_DATABASE_URL"] = "sqlite:///./test_localintel.db"
os.environ["LOCALINTEL_UPLOAD_DIR"] = str(ROOT / "outputs" / "test_uploads")
os.environ["LOCALINTEL_EXPORT_DIR"] = str(ROOT / "outputs" / "test_exports")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db.session import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)
