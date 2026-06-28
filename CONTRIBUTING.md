# Contributing

Thanks for improving LocalIntel AI.

## Local Checks

Run these before opening a merge request:

```bash
cd backend && ruff format app tests && ruff check app tests && pytest
cd frontend && npm run lint && npm run build
```

## Guidelines

- Keep inference offline and CPU-only.
- Do not introduce cloud AI APIs.
- Prefer small, typed modules.
- Add tests for parser, exporter, database, and API behavior.
- Document new model setup requirements in `docs/OFFLINE_SETUP.md`.
