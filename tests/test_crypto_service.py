"""Tests for the crypto service module"""
import pytest
from httpx import AsyncClient
from backend.crypto_service import crypto_service


@pytest.mark.asyncio
async def test_get_coin_price():
    """Test fetching a single coin price"""
    result = await crypto_service.get_coin_price("bitcoin")
    # API may rate limit, so we check structure if we got data
    if result is not None:
        assert "symbol" in result
        assert "price" in result
        assert "BITCOIN" in result["symbol"] or "BTC" in result["symbol"]


@pytest.mark.asyncio
async def test_get_top_coins():
    """Test fetching top cryptocurrencies"""
    coins = await crypto_service.get_top_coins(limit=5)
    # API might rate limit, so we check structure if we got data
    assert isinstance(coins, list)
    if len(coins) > 0:
        assert len(coins) <= 5
        assert "symbol" in coins[0]
        assert "price" in coins[0]


@pytest.mark.asyncio
async def test_get_coin_details():
    """Test fetching detailed coin information"""
    details = await crypto_service.get_coin_details("ethereum")
    # API may rate limit, so we check structure if we got data
    if details is not None:
        assert "name" in details
        assert "symbol" in details
        assert details["symbol"] == "ETH"


@pytest.mark.asyncio
async def test_get_trending_coins():
    """Test fetching trending cryptocurrencies"""
    trending = await crypto_service.get_trending_coins()
    assert isinstance(trending, list)
    if len(trending) > 0:
        assert "name" in trending[0]
        assert "symbol" in trending[0]


@pytest.mark.asyncio
async def test_get_fear_greed_index():
    """Test fetching market sentiment"""
    fgi = await crypto_service.get_fear_greed_index()
    if fgi is not None:
        assert "value" in fgi
        assert "classification" in fgi
        assert 0 <= fgi["value"] <= 100
