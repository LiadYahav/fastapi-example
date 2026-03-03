import os

# Set env vars before importing app modules so pydantic_settings picks them up
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.database import Base, get_db

ASYNC_TEST_URL = "sqlite+aiosqlite:///./test.db"
SYNC_TEST_URL = "sqlite:///./test.db"

# NullPool: never reuse connections across requests — avoids event-loop binding issues
async_engine = create_async_engine(ASYNC_TEST_URL, poolclass=NullPool)
AsyncTestingSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


def _apply_sqlite_now_fix(engine):
    """Replace NOW() with CURRENT_TIMESTAMP in all SQL — needed for SQLite compatibility."""
    @event.listens_for(engine, "before_cursor_execute", retval=True)
    def _fix(conn, cursor, statement, parameters, context, executemany):
        if "NOW()" in statement:
            statement = statement.replace("NOW()", "CURRENT_TIMESTAMP")
        return statement, parameters


@pytest.fixture()
def _session():
    # Sync engine for table management — no event loop needed.
    # The NOW() fix must be applied here so CREATE TABLE stores CURRENT_TIMESTAMP,
    # not NOW() (which SQLite then fails to evaluate during INSERT).
    sync_engine = create_engine(SYNC_TEST_URL, connect_args={"check_same_thread": False})
    _apply_sqlite_now_fix(sync_engine)
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)
    sync_engine.dispose()
    yield
    sync_engine = create_engine(SYNC_TEST_URL, connect_args={"check_same_thread": False})
    Base.metadata.drop_all(bind=sync_engine)
    sync_engine.dispose()


@pytest.fixture()
def client(_session):
    async def override_get_db():
        async with AsyncTestingSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    res = client.post("/users/", json={"email": "user@example.com", "password": "password123"})
    assert res.status_code == 201
    data = res.json()
    data["password"] = "password123"
    return data


@pytest.fixture
def test_user2(client):
    res = client.post("/users/", json={"email": "user2@example.com", "password": "password456"})
    assert res.status_code == 201
    data = res.json()
    data["password"] = "password456"
    return data


@pytest.fixture
def token(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == 200
    return res.json()["access_token"]


@pytest.fixture
def authorized_client(_session, token):
    # Use a separate TestClient so its auth headers don't bleed into the plain `client` fixture
    async def override_get_db():
        async with AsyncTestingSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        c.headers.update({"Authorization": f"Bearer {token}"})
        yield c


@pytest.fixture
def test_posts(authorized_client):
    posts = [
        {"title": "First Post", "content": "Content of first post"},
        {"title": "Second Post", "content": "Content of second post"},
        {"title": "Third Post", "content": "Content of third post"},
    ]
    created = []
    for post in posts:
        res = authorized_client.post("/posts/", json=post)
        assert res.status_code == 201
        created.append(res.json())
    return created
