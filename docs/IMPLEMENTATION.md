# Local Implementation of `.fit` File Upload System

This document outlines the architecture, technologies, and setup steps for a locally deployable web application that enables:

- User registration and authentication  
- Upload of `.fit` files
- Local storage of users and basic metadata (filename, upload date, user ID)

The implementation emphasizes **simplicity**, **maintainability**, and modern technologies—avoiding legacy CMS platforms.

---

## Technology Stack

| Layer               | Technology        | Rationale |
|---------------------|-------------------|----------|
| **Frontend**        | SvelteKit         | Lightweight, performant, and developer-friendly. Excellent for forms and file uploads with minimal boilerplate. |
| **Backend / API**   | FastAPI (Python)  | Built-in support for file uploads (`UploadFile`), automatic OpenAPI docs, strong typing, and easy integration with data processing libraries. |
| **Database**        | SQLite            | Zero-configuration, file-based database. Ideal for local development and MVPs. Easily migratable to PostgreSQL later. |
| **Authentication**  | Email + password with bcrypt hashing | Simple, self-contained auth but extendable to OAuth. |
| **File Storage**    | Local filesystem (`./uploads/`) | `.fit` files are stored as-is on disk, no cloud services or processing. |
| **Local Deployment**| Direct execution or Docker | Supports reproducible environments without internet access. |

> **Key advantage**: Runs entirely offline on a single machine.

---

## Project Structure

```
trail-fit-uploader/
├── backend/
│   ├── main.py              # FastAPI app entrypoint
│   ├── models.py            # SQLAlchemy models (User, Upload)
│   ├── auth.py              # Registration/login logic
│   ├── routes/
│   │   ├── users.py         # Auth endpoints
│   │   └── uploads.py       # File upload endpoint
│   └── database.py          # SQLite DB setup
├── frontend/
│   ├── src/
│   │   ├── routes/
│   │   │   ├── login/       # Login page
│   │   │   ├── register/    # Registration page
│   │   │   └── upload/      # File upload form
│   │   └── lib/
│   │       └── api.js       # API client for backend calls
│   └── svelte.config.js
├── uploads/                 # Directory for uploaded .fit files (not tracked in Git)
├── .gitignore
├── docker-compose.yml       (optional)
├── README.md
└── pyproject.toml          # Python dependencies
```

---

## System Requirements

- Python 3.10+  
- Node.js 18+  
- Docker and Docker Compose

---

## Setup & Run

### 1. Backend setup and build guideline

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux

pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart
```

### 2. Backend entrypoint in docker-compose.yml

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

> API available at port 8000 inside the container and any available port on the host  
> Automatic docs (Swagger UI) available at /docs

### 3. Frontend setup and build guideline

```bash
npm install
npm run dev
```

> Frontend runs on port 5173 inside the container and any available port on the host

### 4. Configure proxy to avoid CORS

In `vite.config.js`:

```js
// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://backend:8000'
    }
  }
});
```

Now frontend requests to `/api/upload` are proxied to the backend.

---

## Implemented Features

### User Registration  
- **Endpoint**: `POST /api/users/register`
- **Fields**: `email`, `password` (hashed with bcrypt)  
- Basic validation for email format and password strength.

### User Login  
- **Endpoint**: `POST /api/users/login`  
- Returns a simple JWT token for session management (local use only).

### `.fit` File Upload  
- **Endpoint**: `POST /api/upload`  
- Requires `Authorization: Bearer <token>` header  
- Validates file extension (only `.fit` allowed)  
- Saves file to `./uploads/{user_id}/{timestamp}.fit`  
- Logs metadata in SQLite: `user_id`, `filename`, `filepath`, `upload_date`

---

## Storage Strategy

- `.fit` files are **not processed or parsed**.  
- Stored on disk under: `./uploads/{user_id}/`  
- SQLite database stores only:
  - User ID
  - Original filename
  - File path on disk
  - Upload timestamp

---

## Security

- Passwords hashed using `bcrypt`  
- Uploads restricted to authenticated users  
- Filename extension validated (`.fit` only)  
- Advanced protections (rate limiting, file scanning).

---

## Final Notes

- Designed for **local research, prototyping, or thesis-related data collection**.  
- **No external services** (AWS, Auth0, etc.) required at this stage.  
