import subprocess  # nosec B404
from pathlib import Path

from app.core.config import get_settings
from app.services.parser import clean_text


def transcribe_audio(path: Path) -> str:
    settings = get_settings()
    output_base = path.with_suffix("")
    command = [
        settings.whisper_cpp_binary,
        "-m",
        str(settings.whisper_model_path),
        "-f",
        str(path),
        "-otxt",
        "-of",
        str(output_base),
        "-t",
        "4",
    ]
    try:
        subprocess.run(  # nosec B603
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=600,
        )
        transcript_path = output_base.with_suffix(".txt")
        return clean_text(transcript_path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return clean_text(
            f"Audio transcription unavailable locally for {path.name}. "
            f"Install whisper.cpp. {exc}"
        )
