import httpx
from typing import Optional, Dict, List
from datetime import datetime


class CryptoService:
    """Service for fetching cryptocurrency data from various APIs"""

    COINGECKO_API = "https://api.coingecko.com/api/v3"
    BINANCE_API = "https://api.binance.com/api/v3"
    BINANCE_FUTURES_API = "https://fapi.binance.com/futures/data"

    # Common ticker → CoinGecko ID mapping (top 100 by market cap + popular)
    TICKER_TO_ID = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "usdt": "tether",
        "usdc": "usd-coin",
        "xrp": "ripple",
        "bnb": "binancecoin",
        "sol": "solana",
        "trx": "tron",
        "doge": "dogecoin",
        "ada": "cardano",
        "leo": "leo-token",
        "bch": "bitcoin-cash",
        "link": "chainlink",
        "xmr": "monero",
        "zec": "zcash",
        "xlm": "stellar",
        "dai": "dai",
        "ltc": "litecoin",
        "avax": "avalanche-2",
        "hbar": "hedera-hashgraph",
        "sui": "sui",
        "shib": "shiba-inu",
        "tao": "bittensor",
        "ton": "the-open-network",
        "cro": "crypto-com-chain",
        "xaut": "tether-gold",
        "paxg": "pax-gold",
        "mnt": "mantle",
        "dot": "polkadot",
        "uni": "uniswap",
        "near": "near",
        "okb": "okb",
        "pi": "pi-network",
        "pepe": "pepe",
        "icp": "internet-computer",
        "aave": "aave",
        "bgb": "bitget-token",
        "etc": "ethereum-classic",
        "ondo": "ondo-finance",
        "gt": "gatechain-token",
        "kcs": "kucoin-shares",
        "qnt": "quant-network",
        "render": "render-token",
        "morpho": "morpho",
        "algo": "algorand",
        "pol": "polygon-ecosystem-token",
        "matic": "polygon-ecosystem-token",
        "atom": "cosmos",
        "nexo": "nexo",
        "kas": "kaspa",
        "wld": "worldcoin-wld",
        "ena": "ethena",
        "fil": "filecoin",
        "trump": "official-trump",
        "apt": "aptos",
        "flr": "flare-networks",
        "xdc": "xdce-crowd-sale",
        "arb": "arbitrum",
        "bdx": "beldex",
        "vet": "vechain",
        "jst": "just",
        "jup": "jupiter-exchange-solana",
        "fet": "fetch-ai",
        "siren": "siren-2",
        "bonk": "bonk",
        "zro": "layerzero",
        "op": "optimism",
        "inj": "injective-protocol",
        "imx": "immutable-x",
        "stx": "blockstack",
        "tia": "celestia",
        "wif": "dogwifcoin",
        "not": "notcoin",
        "hmstr": "hamster-kombat",
        "sei": "sei-network",
        "pendle": "pendle",
        "rune": "thorchain",
        "ftm": "fantom",
        "grt": "the-graph",
        "theta": "theta-token",
        "sand": "the-sandbox",
        "mana": "decentraland",
        "axs": "axie-infinity",
        "egld": "elrond-erd-2",
        "flow": "flow",
        "xtz": "tezos",
        "eos": "eos",
        "klay": "klay-token",
        "mkr": "maker",
        "snx": "havven",
        "cake": "pancakeswap-token",
        "ldo": "lido-dao",
        "crv": "curve-dao-token",
        "comp": "compound-governance-token",
        "sushi": "sushi",
        "bat": "basic-attention-token",
        "zil": "zilliqa",
        "icx": "icon",
        "ont": "ontology",
        "waves": "waves",
        "chz": "chiliz",
        "enJ": "enjincoin",
        "1inch": "1inch",
        "dydx": "dydx",
        "gala": "gala",
        "lunc": "terra-luna",
        "luna": "terra-luna-2",
        "blur": "blur",
        "apt": "aptos",
        "arb": "arbitrum",
        "op": "optimism",
    }

    async def _resolve_coin_id(self, symbol: str) -> str:
        """Convert common ticker symbols to CoinGecko IDs"""
        sym = symbol.lower().strip()
        # Check our mapping first
        if sym in self.TICKER_TO_ID:
            return self.TICKER_TO_ID[sym]
        # Try common full names
        if sym.endswith("coin") or sym.endswith("network") or sym.endswith("chain"):
            return sym
        # Try as-is
        return sym

    async def get_coin_price(self, symbol: str) -> Optional[Dict]:
        """Get current price for a cryptocurrency"""
        try:
            coin_id = await self._resolve_coin_id(symbol)
            async with httpx.AsyncClient() as client:
                # Using CoinGecko with resolved coin_id
                response = await client.get(
                    f"{self.COINGECKO_API}/simple/price",
                    params={
                        "ids": coin_id,
                        "vs_currencies": "usd",
                        "include_24hr_change": "true",
                        "include_24hr_vol": "true",
                        "include_market_cap": "true",
                    },
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    if coin_id in data:
                        return {
                            "symbol": symbol.upper(),
                            "price": data[coin_id].get("usd"),
                            "price_change_24h": data[coin_id].get("usd_24h_change"),
                            "volume_24h": data[coin_id].get("usd_24h_vol"),
                            "market_cap": data[coin_id].get("usd_market_cap"),
                        }
                    # Fallback: try original symbol as key
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
            coin_id = await self._resolve_coin_id(symbol)
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.COINGECKO_API}/coins/{coin_id}",
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
        """Get Crypto Fear & Greed Index - always calculated from real market data"""
        # Alternative.me API returns unreliable values (e.g. 14 when reality is ~42)
        # So we always calculate from real market movements
        return await self._calculate_sentiment_from_market()

    async def _calculate_sentiment_from_market(self) -> Optional[Dict]:
        """Calculate market sentiment from real market data (BTC dominance, volume, price change)"""
        import time
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
                    timeout=15.0,
                )

                if btc_response.status_code != 200:
                    print(f"BTC API returned {btc_response.status_code}")
                    return None

                btc_data = btc_response.json().get("bitcoin", {})
                if not btc_data:
                    print("No BTC data in response")
                    return None
                btc_change_24h = btc_data.get("usd_24h_change", 0) or 0

                # Add a small delay to avoid CoinGecko rate limits
                await __import__("asyncio").sleep(1.5)

                # Get top 10 coins to calculate average market change
                market_response = await client.get(
                    f"{self.COINGECKO_API}/coins/markets",
                    params={
                        "vs_currency": "usd",
                        "order": "market_cap_desc",
                        "per_page": 10,
                        "page": 1,
                    },
                    timeout=15.0,
                )

                if market_response.status_code != 200:
                    print(f"Markets API returned {market_response.status_code}")
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
