import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db


# Test database setup
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


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


class TestUserRegistration:
    def test_register_success(self):
        response = client.post(
            "/api/users/register",
            json={
                "email": "test@example.com",
                "password": "securepassword123",
                "body_weight": 70.5,
                "age": 30,
                "gender": "male",
                "vo2max": 55.0,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["body_weight"] == 70.5
        assert data["age"] == 30
        assert "id" in data

    def test_register_duplicate_email(self):
        client.post(
            "/api/users/register",
            json={"email": "test@example.com", "password": "securepassword123"},
        )
        response = client.post(
            "/api/users/register",
            json={"email": "test@example.com", "password": "anotherpassword123"},
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_invalid_email(self):
        response = client.post(
            "/api/users/register",
            json={"email": "invalid-email", "password": "securepassword123"},
        )
        assert response.status_code == 422

    def test_register_short_password(self):
        response = client.post(
            "/api/users/register",
            json={"email": "test@example.com", "password": "short"},
        )
        assert response.status_code == 422


class TestUserLogin:
    def test_login_success(self):
        # Register first
        client.post(
            "/api/users/register",
            json={"email": "login@example.com", "password": "securepassword123"},
        )
        # Login
        response = client.post(
            "/api/users/login",
            data={"username": "login@example.com", "password": "securepassword123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        client.post(
            "/api/users/register",
            json={"email": "wrongpass@example.com", "password": "securepassword123"},
        )
        response = client.post(
            "/api/users/login",
            data={"username": "wrongpass@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self):
        response = client.post(
            "/api/users/login",
            data={"username": "nonexistent@example.com", "password": "anypassword"},
        )
        assert response.status_code == 401


class TestFileUpload:
    def get_auth_header(self):
        client.post(
            "/api/users/register",
            json={"email": "uploader@example.com", "password": "securepassword123"},
        )
        response = client.post(
            "/api/users/login",
            data={"username": "uploader@example.com", "password": "securepassword123"},
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_upload_without_auth(self):
        response = client.post(
            "/api/upload/",
            files={"file": ("test.fit", b"dummy content", "application/octet-stream")},
        )
        assert response.status_code == 401

    def test_upload_non_fit_file(self):
        headers = self.get_auth_header()
        response = client.post(
            "/api/upload/",
            headers=headers,
            files={"file": ("test.txt", b"dummy content", "text/plain")},
        )
        assert response.status_code == 400
        assert "Only .fit files" in response.json()["detail"]

    def test_upload_success(self, tmp_path, monkeypatch):
        import routers.uploads
        monkeypatch.setattr(routers.uploads, "UPLOAD_DIR", str(tmp_path))

        headers = self.get_auth_header()
        response = client.post(
            "/api/upload/",
            headers=headers,
            files={"file": ("activity.fit", b"FIT file content", "application/octet-stream")},
            data={
                "session_type": "training",
                "fatigue_level": "3",
                "sleep_quality": "4",
                "hydration_status": "well_hydrated",
                "weather_condition": "sunny",
                "trail_condition": "dry",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "activity.fit"
        assert data["session_type"] == "training"
        assert data["fatigue_level"] == 3

    def test_list_uploads(self, tmp_path, monkeypatch):
        import routers.uploads
        monkeypatch.setattr(routers.uploads, "UPLOAD_DIR", str(tmp_path))

        headers = self.get_auth_header()
        # Upload a file first
        client.post(
            "/api/upload/",
            headers=headers,
            files={"file": ("test.fit", b"content", "application/octet-stream")},
        )
        # List uploads
        response = client.get("/api/upload/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["filename"] == "test.fit"
