# Quick Start Guide - SE Crypto Bot

## 🚀 Get Your Bot Running in 5 Minutes

### Step 1: Get Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions:
   - Choose a name for your bot (e.g., "SE Crypto Tracker")
   - Choose a username for your bot (must end in 'bot', e.g., "se_crypto_tracker_bot")
4. **Copy the token** that BotFather gives you (looks like: `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`)

### Step 2: Setup Local Development

```bash
# Navigate to project
cd /Library/ArseniyFolder/se-crypto-project

# Run setup script
./setup.sh

# Edit .env file and add your token
nano .env
# Add this line: TELEGRAM_BOT_TOKEN=your_token_here
```

### Step 3: Start the Services

**Terminal 1 - Backend API:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Telegram Bot:**
```bash
cd bot
source venv/bin/activate
python main.py
```

### Step 4: Test Your Bot

1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. Try commands:
   - `/price bitcoin`
   - `/top 5`
   - `/trending`
   - `/sentiment`

### Step 5: Deploy to University VM (Version 2)

**On your VM:**

```bash
# SSH into your VM
ssh your_username@vm_address

# Clone your GitHub repo (after pushing)
git clone https://github.com/your_username/se-toolkit-hackathon.git
cd se-toolkit-hackathon

# Or copy files directly
scp -r /Library/ArseniyFolder/se-crypto-project/* your_username@vm_address:/path/to/project

# Setup .env file
cp .env.example .env
nano .env  # Add your TELEGRAM_BOT_TOKEN

# Deploy with Docker
sudo docker compose up -d --build

# Check status
sudo docker compose ps
```

## 📋 Task Completion Checklist

### Version 1 (Show to TA during lab):
- [x] Bot responds to `/start` and `/help`
- [x] Bot can fetch crypto prices (`/price bitcoin`)
- [x] Bot can show top coins (`/top 10`)
- [x] Backend API is running
- [x] Database is set up
- [ ] Show to TA and get feedback

### Version 2 (Deploy by deadline):
- [x] All features working locally
- [x] Docker configuration ready
- [ ] Deployed to VM
- [ ] Pushed to GitHub as `se-toolkit-hackathon`
- [ ] README updated with your info
- [ ] Create 5-slide presentation

## 🎯 Presentation (Task 5)

**Slide 1: Title**
- Product: SE Crypto Bot
- Your Name
- University Email
- Your Group

**Slide 2: Context**
- End-user: Crypto traders and enthusiasts
- Problem: Scattered crypto information across platforms
- Solution: One Telegram bot for all crypto data

**Slide 3: Implementation**
- Version 1: Basic bot with price commands
- Version 2: Advanced features + Docker deployment
- TA feedback addressed: [add after receiving feedback]

**Slide 4: Demo**
- Record 2-minute video showing:
  - Starting the bot
  - Getting crypto prices
  - Viewing trending coins
  - Checking market sentiment

**Slide 5: Links**
- GitHub repo: [your repo URL]
- Live bot: [your bot username]

## 🔧 Troubleshooting

### Bot doesn't respond
- Check if TELEGRAM_BOT_TOKEN is correct in .env
- Make sure both backend and bot are running
- Check terminal for error messages

### Can't fetch crypto data
- Check internet connection
- APIs might be rate-limited (wait a minute and try again)
- Check if httpx is installed: `pip install httpx`

### Docker issues
- Stop all containers: `sudo docker compose down`
- Remove old images: `sudo docker compose rm`
- Rebuild: `sudo docker compose up -d --build`

### Database errors
- Delete old database: `rm crypto_bot.db`
- Restart services (database will be recreated)

## 📞 Need Help?

1. Check the main README.md for detailed documentation
2. Review bot/main.py for command implementations
3. Check backend/crypto_service.py for API integrations
4. Look at logs: `sudo docker compose logs -f`

---

**Good luck with your hackathon! 🎉**
