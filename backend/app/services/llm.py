import json
import re
import subprocess  # nosec B404
from collections import Counter
from pathlib import Path
from typing import Any

from app.core.config import get_settings

STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "because",
    "before",
    "being",
    "between",
    "could",
    "from",
    "have",
    "into",
    "only",
    "other",
    "their",
    "there",
    "these",
    "this",
    "through",
    "with",
    "would",
}


def _extract_json(payload: str) -> dict[str, Any] | None:
    match = re.search(r"\{.*\}", payload, flags=re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        return None


def _fallback_metadata(text: str, filename: str, file_type: str) -> dict[str, Any]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text)
    lowered = [word.lower() for word in words if word.lower() not in STOPWORDS]
    keywords = [word for word, _ in Counter(lowered).most_common(10)]
    entities = sorted(set(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)))[:12]
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    summary = (
        " ".join(sentences[:3])[:700]
        if sentences and sentences[0]
        else "No readable text extracted."
    )
    title = (
        sentences[0][:90]
        if sentences and sentences[0]
        else Path(filename).stem.replace("_", " ").title()
    )
    priority = (
        "high"
        if re.search(r"\b(urgent|invoice|contract|deadline|risk|critical)\b", text, re.I)
        else "medium"
    )
    confidence = 0.72 if text and "unavailable locally" not in text else 0.35
    return {
        "title": title,
        "summary": summary,
        "document_type": file_type,
        "keywords": keywords,
        "entities": entities,
        "priority": priority,
        "confidence": confidence,
    }


def generate_metadata(text: str, filename: str, file_type: str) -> dict[str, Any]:
    settings = get_settings()
    prompt = (
        "Return strict JSON with keys title, summary, document_type, keywords, "
        "entities, priority, confidence. Analyze this local document:\n\n"
        f"Filename: {filename}\nType: {file_type}\nText:\n{text[:5000]}"
    )
    command = [
        settings.llama_cpp_binary,
        "-m",
        str(settings.llama_model_path),
        "-p",
        prompt,
        "-n",
        "512",
        "--threads",
        "4",
    ]
    try:
        completed = subprocess.run(  # nosec B603
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=900,
        )
        parsed = _extract_json(completed.stdout)
        if parsed:
            fallback = _fallback_metadata(text, filename, file_type)
            fallback.update(parsed)
            return fallback
    except Exception:
        return _fallback_metadata(text, filename, file_type)
    return _fallback_metadata(text, filename, file_type)
