import httpx
from typing import Optional, Dict, List
from datetime import datetime


class CryptoService:
    """Service for fetching cryptocurrency data from various APIs"""

    COINGECKO_API = "https://api.coingecko.com/api/v3"
    BINANCE_API = "https://api.binance.com/api/v3"
    BINANCE_FUTURES_API = "https://fapi.binance.com/futures/data"

    async def get_coin_price(self, symbol: str) -> Optional[Dict]:
        """Get current price for a cryptocurrency"""
        try:
            async with httpx.AsyncClient() as client:
                # Using CoinGecko
                response = await client.get(
                    f"{self.COINGECKO_API}/simple/price",
                    params={
                        "ids": symbol.lower(),
                        "vs_currencies": "usd",
                        "include_24hr_change": "true",
                        "include_24hr_vol": "true",
                        "include_market_cap": "true",
                    },
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    if symbol.lower() in data:
                        return {
                            "symbol": symbol.upper(),
                            "price": data[symbol.lower()].get("usd"),
                            "price_change_24h": data[symbol.lower()].get("usd_24h_change"),
                            "volume_24h": data[symbol.lower()].get("usd_24h_vol"),
                            "market_cap": data[symbol.lower()].get("usd_market_cap"),
                        }
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
        return None

    async def get_top_coins(self, limit: int = 10) -> List[Dict]:
        """Get top cryptocurrencies by market cap"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.COINGECKO_API}/coins/markets",
                    params={
                        "vs_currency": "usd",
                        "order": "market_cap_desc",
                        "per_page": limit,
                        "page": 1,
                    },
                    timeout=10.0,
                )
                if response.status_code == 200:
                    coins = []
                    for coin in response.json():
                        coins.append(
                            {
                                "symbol": coin["symbol"].upper(),
                                "name": coin["name"],
                                "price": coin["current_price"],
                                "price_change_24h": coin.get("price_change_percentage_24h", 0),
                                "market_cap": coin.get("market_cap", 0),
                                "volume_24h": coin.get("total_volume", 0),
                            }
                        )
                    return coins
        except Exception as e:
            print(f"Error fetching top coins: {e}")
        return []

    async def get_long_short_ratio(self, symbol: str = "BTCUSDT") -> Optional[Dict]:
        """Get long/short ratio from Binance Futures API"""
        try:
            async with httpx.AsyncClient() as client:
                # Use the updated Futures API endpoint (fapi.binance.com)
                response = await client.get(
                    f"{self.BINANCE_FUTURES_API}/globalLongShortAccountRatio",
                    params={"symbol": symbol, "period": "1d", "limit": 1},
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        ratio_data = data[0]
                        long_ratio = float(ratio_data.get("longShortRatio", 0))
                        return {
                            "symbol": symbol,
                            "long_short_ratio": long_ratio,
                            "long_percentage": (long_ratio / (1 + long_ratio)) * 100,
                            "short_percentage": (1 / (1 + long_ratio)) * 100,
                            "timestamp": ratio_data.get("timestamp"),
                        }
        except Exception as e:
            print(f"Error fetching long/short ratio for {symbol}: {e}")
        return None

    async def get_coin_details(self, symbol: str) -> Optional[Dict]:
        """Get detailed information about a cryptocurrency"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.COINGECKO_API}/coins/{symbol.lower()}",
                    params={"localization": "false", "tickers": "false"},
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    market_data = data.get("market_data", {})
                    return {
                        "name": data.get("name"),
                        "symbol": data.get("symbol").upper(),
                        "description": (data.get("description", {}).get("en", "") or "")[:300],
                        "current_price": market_data.get("current_price", {}).get("usd"),
                        "market_cap": market_data.get("market_cap", {}).get("usd"),
                        "market_cap_rank": data.get("market_cap_rank"),
                        "price_change_24h": market_data.get("price_change_percentage_24h"),
                        "price_change_7d": market_data.get("price_change_percentage_7d"),
                        "ath": market_data.get("ath", {}).get("usd"),
                        "circulating_supply": market_data.get("circulating_supply"),
                        "total_supply": market_data.get("total_supply"),
                        "homepage": data.get("links", {}).get("homepage", [""])[0],
                    }
        except Exception as e:
            print(f"Error fetching details for {symbol}: {e}")
        return None

    async def get_trending_coins(self) -> List[Dict]:
        """Get trending cryptocurrencies"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.COINGECKO_API}/search/trending", timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    trending = []
                    for coin in data.get("coins", [])[:7]:
                        item = coin.get("item", {})
                        trending.append(
                            {
                                "name": item.get("name"),
                                "symbol": item.get("symbol"),
                                "market_cap_rank": item.get("market_cap_rank"),
                                "price": item.get("data", {}).get("price"),
                                "price_change_24h": item.get("data", {}).get(
                                    "price_change_percentage_24h", {}
                                ).get("usd"),
                            }
                        )
                    return trending
        except Exception as e:
            print(f"Error fetching trending coins: {e}")
        return []

    async def get_fear_greed_index(self) -> Optional[Dict]:
        """Get Crypto Fear & Greed Index from multiple sources"""
        try:
            # Try Alternative.me API first
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.alternative.me/fng/?limit=1", timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get("data"):
                        fgi = data["data"][0]
                        value = int(fgi.get("value", 0))
                        classification = fgi.get("value_classification", "Unknown")
                        
                        # Check if data seems stale (older than 24 hours OR in the future)
                        import time
                        timestamp = int(fgi.get("timestamp", 0))
                        current_time = int(time.time())
                        time_diff = current_time - timestamp
                        is_stale = (abs(time_diff) > 86400)  # 24 hours in either direction

                        # If data seems stale, calculate our own based on market metrics
                        if is_stale:
                            print(f"Fear & Greed data appears stale (diff: {time_diff}s), calculating from market data...")
                            return await self._calculate_sentiment_from_market()

                        return {
                            "value": value,
                            "classification": classification,
                            "timestamp": timestamp,
                            "source": "alternative.me"
                        }
        except Exception as e:
            print(f"Error fetching fear & greed index from Alternative.me: {e}")
        
        # Fallback: calculate from market data
        print("Falling back to market-based sentiment calculation...")
        return await self._calculate_sentiment_from_market()

    async def _calculate_sentiment_from_market(self) -> Optional[Dict]:
        """Calculate market sentiment from real market data (BTC dominance, volume, price change)"""
        try:
            async with httpx.AsyncClient() as client:
                # Get BTC data
                btc_response = await client.get(
                    f"{self.COINGECKO_API}/simple/price",
                    params={
                        "ids": "bitcoin",
                        "vs_currencies": "usd",
                        "include_24hr_change": "true",
                        "include_market_cap": "true",
                    },
                    timeout=10.0,
                )
                
                if btc_response.status_code != 200:
                    return None
                    
                btc_data = btc_response.json().get("bitcoin", {})
                btc_change_24h = btc_data.get("usd_24h_change", 0) or 0
                btc_market_cap = btc_data.get("usd_market_cap", 0) or 0
                
                # Get top 10 coins to calculate average market change
                market_response = await client.get(
                    f"{self.COINGECKO_API}/coins/markets",
                    params={
                        "vs_currency": "usd",
                        "order": "market_cap_desc",
                        "per_page": 10,
                        "page": 1,
                    },
                    timeout=10.0,
                )
                
                if market_response.status_code != 200:
                    return None
                    
                top_coins = market_response.json()
                avg_change = sum(
                    (coin.get("price_change_percentage_24h") or 0) 
                    for coin in top_coins
                ) / len(top_coins)
                
                # Calculate sentiment score (0-100)
                # Base from BTC 24h change
                # Positive change = higher sentiment, negative = lower
                base_score = 50  # Neutral starting point
                
                # Weight BTC price change heavily (60% weight)
                btc_sentiment = base_score + (btc_change_24h * 2)
                
                # Weight market average change (40% weight)  
                market_sentiment = base_score + (avg_change * 2)
                
                # Combined score
                final_score = (btc_sentiment * 0.6) + (market_sentiment * 0.4)
                
                # Clamp to 0-100
                final_score = max(0, min(100, final_score))
                
                # Classification
                if final_score <= 20:
                    classification = "Extreme Fear"
                elif final_score <= 40:
                    classification = "Fear"
                elif final_score <= 60:
                    classification = "Neutral"
                elif final_score <= 80:
                    classification = "Greed"
                else:
                    classification = "Extreme Greed"
                
                import time
                return {
                    "value": round(final_score),
                    "classification": classification,
                    "timestamp": int(time.time()),
                    "source": "market_calculation",
                    "btc_change_24h": btc_change_24h,
                    "market_avg_change_24h": avg_change
                }
        except Exception as e:
            print(f"Error calculating market-based sentiment: {e}")
            return None


crypto_service = CryptoService()
