from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from database import init_db, get_db
from models import User, UserPreference, PriceHistory
from crypto_service import crypto_service
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="SE Crypto Bot API", version="1.0.0")


@app.on_event("startup")
async def startup():
    await init_db()


class UserCreate(BaseModel):
    telegram_id: str
    username: str = None
    first_name: str = None
    last_name: str = None


class CoinResponse(BaseModel):
    symbol: str
    price: float = None
    price_change_24h: float = None
    market_cap: float = None
    volume_24h: float = None


@app.get("/")
async def root():
    return {"message": "SE Crypto Bot API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.post("/users/", response_model=dict)
async def create_or_update_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register or update a Telegram user"""
    stmt = select(User).where(User.telegram_id == user.telegram_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()

    if db_user:
        db_user.username = user.username
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.last_active = datetime.utcnow()
    else:
        db_user = User(**user.dict())
        db.add(db_user)

    await db.commit()
    return {"message": "User saved", "telegram_id": user.telegram_id}


@app.get("/coins/top", response_model=List[CoinResponse])
async def get_top_coins(limit: int = 10):
    """Get top cryptocurrencies"""
    coins = await crypto_service.get_top_coins(limit)
    return coins


@app.get("/coins/{symbol}")
async def get_coin_info(symbol: str):
    """Get detailed information about a cryptocurrency"""
    coin_data = await crypto_service.get_coin_price(symbol)
    if not coin_data:
        raise HTTPException(status_code=404, detail="Coin not found")
    return coin_data


@app.get("/coins/{symbol}/details")
async def get_coin_details(symbol: str):
    """Get detailed coin information"""
    details = await crypto_service.get_coin_details(symbol)
    if not details:
        raise HTTPException(status_code=404, detail="Coin details not found")
    return details


@app.get("/ratio/{symbol}")
async def get_long_short_ratio(symbol: str = "BTCUSDT"):
    """Get long/short ratio for a trading pair"""
    ratio = await crypto_service.get_long_short_ratio(symbol)
    if not ratio:
        raise HTTPException(status_code=404, detail="Ratio data not found")
    return ratio


@app.get("/trending")
async def get_trending_coins():
    """Get trending cryptocurrencies"""
    return await crypto_service.get_trending_coins()


@app.get("/market/sentiment")
async def get_market_sentiment():
    """Get market sentiment (Fear & Greed Index)"""
    return await crypto_service.get_fear_greed_index()
