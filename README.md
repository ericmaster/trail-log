# Trail Fit Uploader

A local web application for uploading and managing .fit files with detailed session metadata.

## Features

- User registration with athlete profile (weight, age, gender, VO2max)
- Secure authentication with JWT tokens
- .fit file uploads with metadata:
  - Session context (type, race name, notes)
  - Physiological data (fatigue, sleep quality, hydration)
  - Environmental conditions (weather, trail)
- PostgreSQL database for data persistence
- Modern responsive UI with dark theme

## Quick Start

### Prerequisites

- Docker and Docker Compose

### Run the application

```bash
docker-compose up --build
```

Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs

### Development

#### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend (SvelteKit)

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
cd backend
pip install pytest httpx
pytest tests/
```

## Project Structure

```
trail-log/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   ├── routers/
│   │   ├── users.py         # User routes
│   │   └── uploads.py       # Upload routes
│   └── tests/
│       └── test_main.py     # API tests
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   └── api.ts       # API client
│   │   └── routes/
│   │       ├── login/
│   │       ├── register/
│   │       └── upload/
│   └── Dockerfile
├── data/
│   └── uploads/             # Uploaded .fit files
└── docker-compose.yml
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/users/register | Register new user |
| POST | /api/users/login | Login and get token |
| POST | /api/upload/ | Upload .fit file |
| GET | /api/upload/ | List user's uploads |
