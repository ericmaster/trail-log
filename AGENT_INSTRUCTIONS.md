# Agent Instructions for Trail Fit Uploader

## Project Overview
Trail Fit Uploader is a full-stack web application designed to collect and analyze trail running data (.fit files) alongside subjective metrics (fatigue, sensation, etc.). It supports multiple languages (EN/ES).

## Architecture & Technology Stack
- **Frontend**: SvelteKit (Svelte), TypeScript, Bootstrap 5.
- **Backend**: FastAPI (Python), SQLAlchemy, Pydantic.
- **Database**: PostgreSQL.
- **Infrastructure**: Docker Compose.

## Key Directories
- `backend/`: FastAPI application.
  - `models.py`: SQLAlchemy database models.
  - `schemas.py`: Pydantic data validation schemas.
  - `routers/`: API endpoints.
- `frontend/`: SvelteKit application.
  - `src/routes/`: App pages.
  - `src/lib/`: Shared utilities, components, and API client.
  - `src/lib/i18n/`: Localization files (`en.json`, `es.json`).
- `data-collection-protocol.md`: Defines the data fields and protocol requirements.

## Development Workflow
- **Running the App**:
  ```bash
  docker compose up --build -d
  ```
- **Database Changes**:
  - When modifying `models.py`, ensure `docker compose down` and `up` are run to apply changes (unless using Alembic migrations, which are not currently set up).
  - IMPORTANT: The project currently relies on `Base.metadata.create_all(bind=engine)` in `main.py` (or implied startup) for table creation. Adding columns often requires a hard reset or manual migration if data preservation is needed.

## Recent Changes (Session Context)
- **Multilingual Support**: added `src/lib/i18n` with English and Spanish.
- **General Sensation Metric**:
  - Added `general_sensation` (1-5 integer) to `Upload` model in `backend/models.py`.
  - Added validation in `backend/schemas.py`.
  - Updated API route in `backend/routers/uploads.py` to handle the form field.
  - Updated Frontend `src/routes/upload/+page.svelte` to include the radio button input.
  - Added translation keys to `en.json` and `es.json`.

## Coding Standards & Patterns
- **API**: Ensure modifying `models.py`, `schemas.py`, and the router (e.g., `routers/uploads.py`) in sync when adding new fields.
- **Frontend**:
  - Use `svelte-i18n` for all text (`$t("key")`).
  - Use Bootstrap classes for styling.
  - Update `src/lib/api.ts` interfaces when backend types change.
