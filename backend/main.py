from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import users, uploads

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trail Fit Uploader API",
    description="API for uploading and managing .fit files",
    version="1.0.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(uploads.router)


@app.get("/")
def root():
    return {"message": "Trail Fit Uploader API", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
