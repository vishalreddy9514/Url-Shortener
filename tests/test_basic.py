
import pytest
from app.main import app, store

def client():
    # each call returns a fresh test client and clears the store
    app.config["TESTING"] = True
    store._data.clear()
    return app.test_client()

def test_root_health():
    rv = client().get("/")
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "healthy", "service": "URL Shortener API"}


def test_api_health():
    rv = client().get("/api/health")
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "ok"

def test_shorten_and_redirect_and_stats():
    c = client()
    long_url = "https://www.example.com/foo"
    # shorten
    rv = c.post("/api/shorten", json={"url": long_url})
    assert rv.status_code == 201
    data = rv.get_json()
    assert "short_code" in data and "short_url" in data

    code = data["short_code"]
    # redirect (302)
    rv2 = c.get(f"/{code}")
    assert rv2.status_code == 302
    assert rv2.location == long_url

    # stats (clicks == 1)
    rv3 = c.get(f"/api/stats/{code}")
    st = rv3.get_json()
    assert st["url"] == long_url
    assert st["clicks"] == 1
    assert "created_at" in st

def test_missing_url_field():
    rv = client().post("/api/shorten", json={})
    assert rv.status_code == 400

def test_invalid_url():
    rv = client().post("/api/shorten", json={"url": "notaurl"})
    assert rv.status_code == 400

def test_not_found_redirect():
    rv = client().get("/abcdef")
    assert rv.status_code == 404

def test_not_found_stats():
    rv = client().get("/api/stats/abcdef")
    assert rv.status_code == 404
