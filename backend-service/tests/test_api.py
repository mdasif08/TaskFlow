"""
Unit tests for TaskFlow API
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(test_db):
    """Create a test user"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/auth/signup", json=user_data)
    if response.status_code != 200:
        raise Exception(f"Failed to create test user: {response.text}")
    return response.json()

@pytest.fixture
def auth_headers(test_user):
    """Get authentication headers for test user"""
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TaskFlow API is running"}

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_user_signup(test_db):
    """Test user registration"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword"
    }
    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data

def test_user_login(test_user):
    """Test user login"""
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user(auth_headers):
    """Test getting current user info"""
    response = client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_create_task(auth_headers):
    """Test creating a task"""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
        "priority": "medium",
        "assigned_user_id": 1
    }
    response = client.post("/api/tasks", json=task_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "pending"

def test_get_tasks(auth_headers):
    """Test getting tasks list"""
    response = client.get("/api/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert "total" in data

def test_unauthorized_access():
    """Test unauthorized access to protected endpoints"""
    response = client.get("/api/users/me")
    assert response.status_code == 401
