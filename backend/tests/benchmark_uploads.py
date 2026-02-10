import time
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set DATABASE_URL to sqlite in-memory BEFORE importing main or database
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from database import Base, get_db
import models
from auth import get_current_user

# Setup in-memory DB - we can reuse the engine from database.py if it picked up the env var,
# or create a new one to be safe and ensure check_same_thread=False for sqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def benchmark():
    # Setup DB
    Base.metadata.create_all(bind=engine)

    # Create user
    db = TestingSessionLocal()
    user = models.User(email="bench@example.com", hashed_password="hashedpassword")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Override auth to return our test user
    app.dependency_overrides[get_current_user] = lambda: user

    # Insert 1000 uploads
    print("Seeding database with 1000 uploads...")
    uploads = []
    for i in range(1000):
        uploads.append(models.Upload(
            user_id=user.id,
            filename=f"file_{i}.fit",
            filepath=f"/tmp/file_{i}.fit",
            session_type="training",
            fatigue_level=3
        ))
    db.add_all(uploads)
    db.commit()

    # Benchmark
    print("Starting benchmark...")
    start_time = time.time()
    response = client.get("/api/upload/")
    end_time = time.time()

    print(f"Status Code: {response.status_code}")
    print(f"Items returned: {len(response.json())}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")

    # Clean up
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    benchmark()
