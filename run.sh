#!/bin/bash

echo "🚀 Starting SE Crypto Bot..."
echo ""

# Check if .env has token
if grep -q "your_bot_token_here" .env 2>/dev/null; then
    echo "❌ ERROR: You need to add your Telegram bot token!"
    echo ""
    echo "📖 Steps:"
    echo "1. Message @BotFather on Telegram"
    echo "2. Send /newbot and follow instructions"
    echo "3. Copy the token you receive"
    echo "4. Edit .env file and replace 'your_bot_token_here' with your token"
    echo ""
    echo "📝 Quick guide: cat GET_TELEGRAM_TOKEN.md"
    exit 1
fi

if [ ! -f .env ] || ! grep -q "TELEGRAM_BOT_TOKEN=" .env 2>/dev/null; then
    echo "❌ ERROR: .env file not found or TELEGRAM_BOT_TOKEN not set!"
    echo ""
    echo "📝 Create .env file with your bot token:"
    echo "   TELEGRAM_BOT_TOKEN=your_token_here"
    echo ""
    echo "📖 See GET_TELEGRAM_TOKEN.md for help"
    exit 1
fi

echo "✅ Bot token found!"
echo ""

# Start backend
echo "📡 Starting backend API..."
cd backend
source venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
cd ..

sleep 2

# Check if backend started
if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running!"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🤖 Starting Telegram Bot..."
cd bot
source venv/bin/activate
python main.py &
BOT_PID=$!
cd ..

echo ""
echo "✅ Both services started!"
echo ""
echo "📊 Backend API: http://127.0.0.1:8000"
echo "🤖 Bot: Running (check Telegram)"
echo ""
echo "💡 To stop: kill $BACKEND_PID $BOT_PID"
echo "   Or just close this terminal"
echo ""

# Wait for processes
wait
