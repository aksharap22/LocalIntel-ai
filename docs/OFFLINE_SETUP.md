# Offline Setup Guide

LocalIntel AI does not download models at runtime.

## Required Local Files

```text
models/
  llm/
    model.gguf
  whisper/
    ggml-base.en.bin
```

## Runtime Binaries

Install CPU builds of:

- `llama-cli` from llama.cpp
- `whisper-cli` from whisper.cpp

Configure custom paths with environment variables:

```bash
export LOCALINTEL_LLAMA_CPP_BINARY=/path/to/llama-cli
export LOCALINTEL_LLAMA_MODEL_PATH=/path/to/model.gguf
export LOCALINTEL_WHISPER_CPP_BINARY=/path/to/whisper-cli
export LOCALINTEL_WHISPER_MODEL_PATH=/path/to/ggml-base.en.bin
```

PaddleOCR and ONNX Runtime are installed as Python CPU packages.
