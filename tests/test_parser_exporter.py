from pathlib import Path

from app.services.llm import generate_metadata
from app.services.parser import clean_text, detect_file_type, extract_document_text


def test_clean_text_normalizes_whitespace():
    assert clean_text(" hello   world \n\n again ") == "hello world\nagain"


def test_detect_file_type():
    assert detect_file_type(Path("memo.pdf")) == "document"
    assert detect_file_type(Path("scan.png")) == "image"
    assert detect_file_type(Path("voice.mp3")) == "audio"


def test_text_parser(tmp_path):
    path = tmp_path / "note.txt"
    path.write_text("Local CPU inference\nworks offline", encoding="utf-8")
    assert extract_document_text(path) == "Local CPU inference\nworks offline"


def test_fallback_metadata_extracts_keywords_and_entities():
    metadata = generate_metadata(
        "Critical roadmap memo for Grace Hopper and Alan Turing. Offline analytics are important.",
        "roadmap.txt",
        "document",
    )
    assert metadata["priority"] == "high"
    assert "Grace Hopper" in metadata["entities"]
    assert metadata["keywords"]
