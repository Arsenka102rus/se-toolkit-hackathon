# SE Crypto Bot

A Telegram bot that provides real-time cryptocurrency market information, including prices, market data, long/short ratios, and market sentiment.

## Demo

**Bot Commands in Action:**

```
/start - Welcome message with available commands
/price bitcoin - Get current BTC price with market data
/top 5 - Get top 5 cryptocurrencies
/details ethereum - Get detailed ETH information
/ratio BTCUSDT - Get long/short ratio for BTC
/trending - Get trending cryptocurrencies
/sentiment - Get market fear & greed index
```

**Example Output:**
```
💰 BTC
💵 Price: $68,543.21
📈 24h Change: +2.34%
💎 Market Cap: $1,345,678,901,234
📊 24h Volume: $28,456,789,012
```

## Product Context

### End Users
- Cryptocurrency traders and investors
- People interested in crypto market trends
- Students learning about cryptocurrency markets

### Problem Solved
Cryptocurrency information is scattered across multiple platforms (CoinGecko, Binance, Alternative.me). Users need to visit multiple websites to get comprehensive market data. This bot aggregates all essential information in one place, accessible through Telegram.

### Our Solution
A Telegram bot that provides:
- Real-time crypto prices and market data
- Long/short trading ratios from Binance
- Market sentiment analysis (Fear & Greed Index)
- Trending cryptocurrencies
- Detailed coin information and statistics

All accessible through simple Telegram commands with formatted responses.

## Features

### ✅ Implemented Features
- **Price Tracking** - Get current prices for any cryptocurrency
- **Top Cryptocurrencies** - View top coins by market cap
- **Detailed Coin Info** - Comprehensive information about any coin
- **Long/Short Ratios** - See trader positioning from Binance
- **Trending Coins** - Discover what's popular right now
- **Market Sentiment** - Fear & Greed Index for market mood
- **SQLite Database** - Stores user data and price history
- **REST API** - FastAPI backend for future web interface
- **Docker Support** - Easy deployment with docker-compose

### 🚧 Future Enhancements
- Price alerts and notifications
- Portfolio tracking
- Historical price charts
- Telegram inline keyboard menus
- Multi-language support
- Company crypto holdings info
- DeFi analytics

## Usage

### Getting Started

1. **Get a Telegram Bot Token:**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow the instructions
   - Copy the bot token you receive

2. **Configure the Bot:**
   ```bash
   cp .env.example .env
   # Edit .env and add your TELEGRAM_BOT_TOKEN
   ```

3. **Run Locally (Development):**

   Start the backend API:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Start the Telegram bot (in another terminal):
   ```bash
   cd bot
   pip install -r requirements.txt
   python main.py
   ```

4. **Use the Bot:**
   - Open Telegram and search for your bot
   - Send `/start` to begin
   - Use commands like `/price bitcoin`, `/top 10`, `/trending`

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message and introduction | `/start` |
| `/help` | Show all available commands | `/help` |
| `/price <coin>` | Get current price and market data | `/price ethereum` |
| `/top [n]` | Get top N cryptocurrencies | `/top 5` |
| `/details <coin>` | Get detailed coin information | `/details solana` |
| `/ratio <pair>` | Get long/short trading ratio | `/ratio BTCUSDT` |
| `/trending` | Get trending cryptocurrencies | `/trending` |
| `/sentiment` | Get market fear & greed index | `/sentiment` |

## Deployment

### Requirements
- **OS:** Ubuntu 24.04 (or any Linux with Docker support)
- **Docker:** Version 20.10 or higher
- **Docker Compose:** Version 2.0 or higher
- **Telegram Bot Token:** From @BotFather

### Step-by-Step Deployment

1. **Install Docker and Docker Compose:**
   ```bash
   # Update package list
   sudo apt update

   # Install prerequisites
   sudo apt install -y ca-certificates curl gnupg

   # Add Docker's official GPG key
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg

   # Add Docker repository
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

   # Install Docker
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

2. **Clone the Repository:**
   ```bash
   git clone <your-repo-url>
   cd se-crypto-project
   ```

3. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env file and add your Telegram bot token
   nano .env
   ```

4. **Build and Start Services:**
   ```bash
   # Build and run both services
   sudo docker compose up -d --build

   # Check if services are running
   sudo docker compose ps

   # View logs
   sudo docker compose logs -f
   ```

5. **Verify Deployment:**
   - Backend API should be accessible at: `http://your-vm-ip:8000`
   - Test your bot in Telegram - it should respond to commands

6. **Stop Services (if needed):**
   ```bash
   sudo docker compose down
   ```

### API Endpoints

The backend provides REST API endpoints:

- `GET /` - API status
- `GET /health` - Health check
- `GET /coins/top?limit=10` - Top cryptocurrencies
- `GET /coins/{symbol}` - Get coin price
- `GET /coins/{symbol}/details` - Detailed coin info
- `GET /ratio/{symbol}` - Long/short ratio
- `GET /trending` - Trending coins
- `GET /market/sentiment` - Fear & Greed Index

## Project Structure

```
se-crypto-project/
├── backend/                 # FastAPI backend service
│   ├── main.py             # API endpoints
│   ├── models.py           # Database models
│   ├── database.py         # Database configuration
│   ├── crypto_service.py   # Crypto data fetching
│   └── requirements.txt    # Python dependencies
├── bot/                    # Telegram bot
│   ├── main.py            # Bot commands and handlers
│   └── requirements.txt   # Python dependencies
├── docker/                 # Docker configurations
│   ├── Dockerfile.backend # Backend Docker image
│   └── Dockerfile.bot     # Bot Docker image
├── docker-compose.yml      # Docker Compose configuration
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Technology Stack

- **Backend:** FastAPI (Python 3.11)
- **Database:** SQLite with SQLAlchemy ORM
- **Telegram Bot:** python-telegram-bot library
- **Data Sources:**
  - CoinGecko API (prices and market data)
  - Binance API (long/short ratios)
  - Alternative.me API (Fear & Greed Index)
- **Deployment:** Docker & Docker Compose
- **Version Control:** Git & GitHub

## Data Sources

This bot aggregates data from multiple free APIs:

1. **CoinGecko** - Cryptocurrency prices, market cap, and details
2. **Binance** - Long/short trading ratios
3. **Alternative.me** - Crypto Fear & Greed Index

## Development

### Running Tests
```bash
# Test backend API
curl http://localhost:8000/health

# Test bot (manually in Telegram)
# Send commands to your bot and verify responses
```

### Code Structure
- `backend/` - REST API and data services
- `bot/` - Telegram bot implementation
- `docker/` - Containerization files
- `data/` - Database files (gitignored)

## License

This project is licensed under the MIT License - see below for details.

```
MIT License

Copyright (c) 2024 SE Crypto Bot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Author

- Kosishnov Arseniy
- a.kosishnov@innopolis.university
- B25-DSAI-05

## Acknowledgments

- CoinGecko for free crypto market data API
- Binance for trading ratio data
- python-telegram-bot library
- FastAPI framework
