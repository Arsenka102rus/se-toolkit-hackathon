#!/bin/bash
echo "🚀 Deploying SE Crypto Bot to VM..."

# Update system
apt update && apt upgrade -y

# Install Docker
apt install -y docker.io docker-compose

# Start and enable Docker
systemctl start docker
systemctl enable docker

# Clone repository
cd /root
git clone https://github.com/Arsenka102rus/se-toolkit-hackathon.git
cd se-toolkit-hackathon

# Set up environment
cp .env.example .env

echo ""
echo "⚠️  NOW EDIT .env and add your Telegram bot token!"
echo "   nano .env"
echo "   Add: TELEGRAM_BOT_TOKEN=your_token_here"
echo ""
read -p "Press Enter after you've added the token..."

# Deploy with Docker
docker-compose up -d --build

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📊 Check status: docker-compose ps"
echo "📋 View logs: docker-compose logs -f"
echo ""
echo "Your bot should now be running on Telegram!"
