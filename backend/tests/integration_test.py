#!/usr/bin/env python3
"""Integration test script for Trail Fit Uploader API."""
import requests
import tempfile
import os
import sys

BASE_URL = os.getenv("API_URL", "http://localhost:8000")
TEST_EMAIL = "integration_test@example.com"
TEST_PASSWORD = "testpassword123"


def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    resp = requests.get(f"{BASE_URL}/health")
    assert resp.status_code == 200, f"Health check failed: {resp.text}"
    assert resp.json()["status"] == "healthy"
    print("✓ Health check passed")


def test_registration():
    """Test user registration."""
    print("Testing user registration...")
    resp = requests.post(
        f"{BASE_URL}/api/users/register",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "body_weight": 70.5,
            "age": 30,
            "gender": "male",
            "vo2max": 55.0,
        },
    )
    if resp.status_code == 400 and "already registered" in resp.text:
        print("✓ User already exists (skipping registration)")
        return
    assert resp.status_code == 201, f"Registration failed: {resp.text}"
    data = resp.json()
    assert data["email"] == TEST_EMAIL
    print("✓ Registration passed")


def test_login() -> str:
    """Test user login and return token."""
    print("Testing user login...")
    resp = requests.post(
        f"{BASE_URL}/api/users/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    data = resp.json()
    assert "access_token" in data
    print("✓ Login passed")
    return data["access_token"]


def test_upload(token: str):
    """Test file upload with metadata."""
    print("Testing file upload...")
    
    # Create a dummy .fit file
    with tempfile.NamedTemporaryFile(suffix=".fit", delete=False) as f:
        f.write(b"FIT DUMMY FILE CONTENT")
        temp_path = f.name
    
    try:
        with open(temp_path, "rb") as f:
            resp = requests.post(
                f"{BASE_URL}/api/upload/",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("test_activity.fit", f, "application/octet-stream")},
                data={
                    "session_type": "training",
                    "race_name": "",
                    "notes": "Integration test upload",
                    "fatigue_level": "2",
                    "sleep_quality": "4",
                    "hydration_status": "well_hydrated",
                    "weather_condition": "sunny",
                    "trail_condition": "dry",
                },
            )
        
        assert resp.status_code == 201, f"Upload failed: {resp.text}"
        data = resp.json()
        assert data["filename"] == "test_activity.fit"
        assert data["session_type"] == "training"
        print("✓ Upload passed")
    finally:
        os.unlink(temp_path)


def test_list_uploads(token: str):
    """Test listing uploads."""
    print("Testing list uploads...")
    resp = requests.get(
        f"{BASE_URL}/api/upload/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200, f"List uploads failed: {resp.text}"
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    print(f"✓ List uploads passed ({len(data)} uploads found)")


def test_upload_without_auth():
    """Test that upload without auth fails."""
    print("Testing upload without authentication...")
    with tempfile.NamedTemporaryFile(suffix=".fit", delete=False) as f:
        f.write(b"DUMMY")
        temp_path = f.name
    
    try:
        with open(temp_path, "rb") as f:
            resp = requests.post(
                f"{BASE_URL}/api/upload/",
                files={"file": ("test.fit", f, "application/octet-stream")},
            )
        assert resp.status_code == 401, f"Expected 401, got {resp.status_code}"
        print("✓ Unauthenticated upload correctly rejected")
    finally:
        os.unlink(temp_path)


def test_upload_non_fit_file(token: str):
    """Test that non-.fit files are rejected."""
    print("Testing non-.fit file rejection...")
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"TEXT CONTENT")
        temp_path = f.name
    
    try:
        with open(temp_path, "rb") as f:
            resp = requests.post(
                f"{BASE_URL}/api/upload/",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("test.txt", f, "text/plain")},
            )
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
        assert "Only .fit files" in resp.text
        print("✓ Non-.fit file correctly rejected")
    finally:
        os.unlink(temp_path)


def main():
    print(f"\n🏃 Running integration tests against {BASE_URL}\n")
    print("=" * 50)
    
    try:
        test_health()
        test_registration()
        token = test_login()
        test_upload(token)
        test_list_uploads(token)
        test_upload_without_auth()
        test_upload_non_fit_file(token)
        
        print("=" * 50)
        print("\n✅ All integration tests passed!\n")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except requests.RequestException as e:
        print(f"\n❌ Network error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
