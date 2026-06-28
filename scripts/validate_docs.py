from pathlib import Path

REQUIRED = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "docs/PROJECT_SPECIFICATION.md",
    "docs/ARCHITECTURE.md",
    "docs/INSTALLATION.md",
    "docs/OFFLINE_SETUP.md",
    "docs/API.md",
    "docs/USER_GUIDE.md",
]

missing = [path for path in REQUIRED if not Path(path).exists()]
if missing:
    raise SystemExit(f"Missing documentation files: {', '.join(missing)}")
