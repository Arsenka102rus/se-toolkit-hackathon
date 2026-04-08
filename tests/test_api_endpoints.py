"""Tests for the FastAPI backend endpoints"""
import pytest
import sys
import os
from httpx import AsyncClient, ASGITransport

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test the root endpoint returns status message"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


@pytest.mark.asyncio
async def test_health_check():
    """Test the health endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_get_top_coins():
    """Test the top coins endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/coins/top?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # API may rate limit, so we check structure if we got data
        if len(data) > 0:
            assert "symbol" in data[0]


@pytest.mark.asyncio
async def test_get_trending_coins():
    """Test the trending coins endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/trending")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_market_sentiment():
    """Test the market sentiment endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/market/sentiment")
        assert response.status_code == 200
        data = response.json()
        if data is not None:
            assert "value" in data
            assert "classification" in data


@pytest.mark.asyncio
async def test_register_user():
    """Test user registration endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/users/",
            json={
                "telegram_id": "test_user_123",
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
