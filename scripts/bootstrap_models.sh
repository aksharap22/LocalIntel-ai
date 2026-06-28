#!/usr/bin/env bash
set -euo pipefail

mkdir -p models/llm models/whisper
cat <<'MSG'
Place CPU-compatible local models here:

models/llm/model.gguf
  A llama.cpp-compatible GGUF instruction model.

models/whisper/ggml-base.en.bin
  A whisper.cpp-compatible model file.

This script intentionally does not download models so the project remains offline-first.
MSG
