# 🚀 How to Get Your Telegram Bot Token

## Step 1: Create Your Bot

1. **Open Telegram** on your phone or computer
2. **Search for:** `@BotFather` (official Telegram bot)
3. **Start a chat** with BotFather
4. **Send:** `/newbot`

## Step 2: Follow BotFather's Instructions

BotFather will ask you:

1. **Choose a name** for your bot
   - Example: `SE Crypto Tracker`
   - This is what users see in chat
   
2. **Choose a username** for your bot
   - Must end with `bot` 
   - Example: `se_crypto_info_bot` or `my_crypto_helper_bot`
   - This is unique and must be available

3. **BotFather will give you a token**
   - Looks like: `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`
   - **COPY THIS TOKEN** - you need it!

## Step 3: Add Token to Your Project

1. **Open** `/Library/ArseniyFolder/se-crypto-project/.env`
2. **Add this line:**
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```
   
   Replace `your_token_here` with the actual token from BotFather.

## Step 4: Run Your Bot

**Terminal 1 - Backend (already running! ✅):**
```bash
cd /Library/ArseniyFolder/se-crypto-project/backend
source venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 - Bot:**
```bash
cd /Library/ArseniyFolder/se-crypto-project/bot
source venv/bin/activate
python main.py
```

## Step 5: Test Your Bot!

1. Open Telegram
2. Search for your bot username (e.g., `se_crypto_info_bot`)
3. Click **Start** or send `/start`
4. Try these commands:
   - `/price bitcoin` - Get BTC price
   - `/top 5` - Top 5 cryptocurrencies  
   - `/trending` - What's trending
   - `/sentiment` - Market mood

## Example Bot Output:

When you send `/price bitcoin`, you'll get:
```
💰 BITCOIN
💵 Price: $71,453.00
📈 24h Change: +2.95%
💎 Market Cap: $1,430,044,203,381
📊 24h Volume: $53,152,752,585
```

## Troubleshooting:

**Bot doesn't respond:**
- Check if `.env` file has the correct token
- Make sure bot is running in terminal (no errors)
- Check if backend is running on port 8000

**Token is wrong:**
- Get a new one from @BotFather
- Send `/mybots` to see all your bots

**Need a new token:**
- Message @BotFather
- Send `/mybots`
- Select your bot
- Click "API Token"

---

**Your backend is already running and working! 🎉**
Just get the token from BotFather and start the bot!
