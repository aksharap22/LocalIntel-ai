#!/usr/bin/env python3
"""Download the offline AI model files used by LocalIntel AI.

Idempotent: skips files that already exist on disk. Safe to re-run.

Models (CPU-friendly, instruction-tuned, ~1 GB total):
  * llama.cpp  -> models/llm/model.gguf
      Source: TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF (tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf)
      Size:    ~700 MB
  * whisper.cpp -> models/whisper/ggml-base.en.bin
      Source:ggerganov/whisper.cpp · resolve/main/ggml-base.en.bin
      Size:    ~140 MB

Override defaults via env vars:
  LOCALINTEL_LLAMA_REPO_ID    (default: TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)
  LOCALINTEL_LLAMA_FILENAME   (default: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf)
  LOCALINTEL_WHISPER_URL      (default: ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin)

Usage:
    python scripts/download_models.py
    python scripts/download_models.py --llm-only
    python scripts/download_models.py --whisper-only
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Repo root = parent of this script's parent
REPO_ROOT = Path(__file__).resolve().parent.parent
LLM_DIR = REPO_ROOT / "models" / "llm"
WHISPER_DIR = REPO_ROOT / "models" / "whisper"

DEFAULT_LLAMA_REPO = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
DEFAULT_LLAMA_FILE = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
DEFAULT_WHISPER_URL = (
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"
)


def _human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def download_llm() -> Path:
    """Download the llama.cpp GGUF model. Returns the local path."""
    from huggingface_hub import hf_hub_download

    LLM_DIR.mkdir(parents=True, exist_ok=True)
    repo_id = os.getenv("LOCALINTEL_LLAMA_REPO_ID", DEFAULT_LLAMA_REPO)
    filename = os.getenv("LOCALINTEL_LLAMA_FILENAME", DEFAULT_LLAMA_FILE)
    target = LLM_DIR / "model.gguf"

    if target.exists() and target.stat().st_size > 100_000_000:  # >100 MB sanity
        print(f"  ✓ llama model already present at {target} ({_human(target.stat().st_size)})")
        return target

    print(f"  ⇣ downloading {repo_id}/{filename} → {target}")
    cached = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=str(LLM_DIR),
        local_dir_use_symlinks=False,
    )
    # hf_hub_download places file at <local_dir>/<filename>; symlink/copy to model.gguf
    cached_path = Path(cached)
    if cached_path != target:
        if target.exists() or target.is_symlink():
            target.unlink()
        target.symlink_to(cached_path)
    print(f"  ✓ llama model downloaded ({_human(target.stat().st_size)})")
    return target


def download_whisper() -> Path:
    """Download the whisper.cpp ggml-base.en.bin model. Returns the local path."""
    import urllib.request

    WHISPER_DIR.mkdir(parents=True, exist_ok=True)
    target = WHISPER_DIR / "ggml-base.en.bin"
    url = os.getenv("LOCALINTEL_WHISPER_URL", DEFAULT_WHISPER_URL)

    if target.exists() and target.stat().st_size > 100_000_000:  # >100 MB sanity
        print(f"  ✓ whisper model already present at {target} ({_human(target.stat().st_size)})")
        return target

    print(f"  ⇣ downloading {url} → {target}")
    tmp = target.with_suffix(target.suffix + ".part")
    try:
        with urllib.request.urlopen(url, timeout=600) as resp, tmp.open("wb") as fh:
            total = int(resp.headers.get("Content-Length", "0"))
            done = 0
            chunk = 1024 * 1024  # 1 MB
            while True:
                block = resp.read(chunk)
                if not block:
                    break
                fh.write(block)
                done += len(block)
                if total:
                    pct = done * 100 / total
                    print(
                        f"    {_human(done)} / {_human(total)}  ({pct:5.1f}%)",
                        end="\r",
                        flush=True,
                    )
        tmp.replace(target)
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise
    print(f"\n  ✓ whisper model downloaded ({_human(target.stat().st_size)})")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--llm-only", action="store_true", help="Download only the llama.cpp model")
    group.add_argument("--whisper-only", action="store_true", help="Download only the whisper model")
    args = parser.parse_args()

    print(f"LocalIntel AI model bootstrap (target: {REPO_ROOT})")

    try:
        if not args.whisper_only:
            download_llm()
        if not args.llm_only:
            download_whisper()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    except Exception as exc:
        print(f"\n✗ download failed: {exc}", file=sys.stderr)
        print(
            "  hint: place model files manually under models/llm/model.gguf and "
            "models/whisper/ggml-base.en.bin to skip network downloads.",
            file=sys.stderr,
        )
        return 1

    print("All models ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
