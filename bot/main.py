import os
import sys
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.crypto_service import crypto_service
from bot.database_helper import db

load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    # Register user in database
    user = update.effective_user
    await db.register_user(
        telegram_id=str(user.id),
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    await db.log_command(str(user.id), "/start")

    welcome_message = (
        "👋 *Welcome to SE Crypto Bot!*\n\n"
        "I can help you get cryptocurrency information:\n\n"
        "📊 *Commands:*\n"
        "/price <coin> - Get current price\n"
        "/top [number] - Get top cryptocurrencies\n"
        "/details <coin> - Get detailed coin info\n"
        "/ratio <pair> - Get long/short ratio\n"
        "/trending - Get trending coins\n"
        "/sentiment - Get market sentiment\n"
        "/help - Show this help message\n\n"
        "Example: `/price bitcoin` or `/top 5`"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    help_text = (
        "🤖 *SE Crypto Bot Help*\n\n"
        "*Available Commands:*\n"
        "• `/price <coin>` - Get current price (e.g., /price btc)\n"
        "• `/top [n]` - Get top N cryptocurrencies (default: 10)\n"
        "• `/details <coin>` - Get detailed information about a coin\n"
        "• `/ratio <pair>` - Get long/short ratio (e.g., /ratio BTCUSDT)\n"
        "• `/trending` - Get currently trending cryptocurrencies\n"
        "• `/sentiment` - Get market fear & greed index\n"
        "• `/help` - Show this help message\n\n"
        "*Examples:*\n"
        "`/price ethereum`\n"
        "`/top 5`\n"
        "`/details solana`\n"
        "`/ratio ETHUSDT`"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get cryptocurrency price."""
    if not context.args:
        await update.message.reply_text(
            "❌ Please specify a coin symbol. Example: `/price bitcoin`",
            parse_mode="Markdown",
        )
        return
    
    coin = " ".join(context.args).lower()
    await send_coin_info(update, coin, context, "/price")


async def send_coin_info(update: Update, coin: str, context: ContextTypes.DEFAULT_TYPE, source: str):
    """Helper to fetch and send coin info"""
    user = update.effective_user
    await db.log_command(str(user.id), source)

    await update.message.reply_text(f"🔍 Fetching info for {coin}...")

    coin_data = await crypto_service.get_coin_price(coin)

    if coin_data:
        price_text = (
            f"💰 *{coin_data['symbol']}*\n\n"
            f"💵 Price: `${coin_data['price']:,.2f}`\n"
            f"📈 24h Change: `{coin_data['price_change_24h']:+.2f}%`\n"
        )
        if coin_data.get('market_cap') and coin_data['market_cap'] > 0:
            price_text += f"💎 Market Cap: `${coin_data['market_cap']:,.0f}`\n"
        price_text += f"📊 24h Volume: `${coin_data['volume_24h']:,.0f}`"
        await update.message.reply_text(price_text, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            f"❌ Could not find price for '{coin}'. Please check the ticker."
        )

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle plain text messages as coin price lookups (default behavior)."""
    text = update.message.text.strip()
    if not text:
        return
    
    # Treat any non-empty text as a coin/ticker lookup
    await send_coin_info(update, text.lower(), context, f"text:{text}")


async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get top cryptocurrencies."""
    user = update.effective_user
    await db.log_command(str(user.id), "/top")

    limit = 10
    if context.args and context.args[0].isdigit():
        limit = min(int(context.args[0]), 20)  # Cap at 20

    await update.message.reply_text(f"🔍 Fetching top {limit} cryptocurrencies...")

    coins = await crypto_service.get_top_coins(limit)

    if coins:
        top_text = "🏆 *Top Cryptocurrencies*\n\n"
        for i, coin in enumerate(coins[:limit], 1):
            change = coin.get("price_change_24h", 0) or 0
            change_symbol = "🟢" if change >= 0 else "🔴"
            top_text += (
                f"{i}. *{coin['symbol']}* - `${coin['price']:,.2f}` {change_symbol}\n"
                f"   24h: `{change:+.2f}%` | MC: `${coin['market_cap']:,.0f}`\n\n"
            )

        # Split message if too long
        if len(top_text) > 4000:
            for chunk in [top_text[i:i+4000] for i in range(0, len(top_text), 4000)]:
                await update.message.reply_text(chunk, parse_mode="Markdown")
        else:
            await update.message.reply_text(top_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Could not fetch top coins. Please try again later.")


async def details_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get detailed coin information."""
    user = update.effective_user
    await db.log_command(str(user.id), "/details")

    if not context.args:
        await update.message.reply_text(
            "❌ Please specify a coin symbol. Example: `/details bitcoin`",
            parse_mode="Markdown",
        )
        return

    coin = " ".join(context.args).lower()
    await update.message.reply_text(f"🔍 Fetching details for {coin}...")

    details = await crypto_service.get_coin_details(coin)

    if details:
        details_text = (
            f"📊 *{details['name']} ({details['symbol']})*\n\n"
            f"💵 Price: `${details['current_price']:,.2f}`\n"
            f"📈 24h Change: `{details['price_change_24h']:+.2f}%`\n"
            f"📅 7d Change: `{details['price_change_7d']:+.2f}%`\n"
            f"💎 Market Cap: `${details['market_cap']:,.0f}` (Rank #{details['market_cap_rank']})\n"
            f"🔄 Circulating Supply: `{details['circulating_supply']:,.0f}`\n"
            f"📦 Total Supply: `{details['total_supply']:,.0f}`\n"
            f"🏆 All-Time High: `${details['ath']:,.2f}`\n\n"
        )

        if details.get("description"):
            details_text += f"📝 *About:*\n{details['description']}\n\n"

        if details.get("homepage"):
            details_text += f"🔗 Website: {details['homepage']}"

        await update.message.reply_text(details_text, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            f"❌ Could not find details for '{coin}'. Please check the symbol."
        )


async def ratio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get long/short ratio. Defaults to USDT pair if none provided."""
    user = update.effective_user
    await db.log_command(str(user.id), "/ratio")

    # Default base symbol and pair suffix
    base_symbol = "BTC"
    pair_suffix = "USDT"  # Default pair suffix, can be changed

    if context.args:
        raw_arg = "".join(context.args).upper()
        # Check if user specified a different pair suffix
        known_suffixes = ["USDT", "BUSD", "USDC"]
        
        # Try to extract base symbol by removing known pair suffixes
        suffix_found = False
        for suffix in known_suffixes:
            if raw_arg.endswith(suffix):
                extracted_base = raw_arg[:-len(suffix)]
                if extracted_base:  # Make sure there's actually a base symbol
                    base_symbol = extracted_base
                    pair_suffix = suffix
                    suffix_found = True
                    break
        
        # If no pair suffix found, treat the whole thing as base symbol with USDT
        if not suffix_found:
            base_symbol = raw_arg
            pair_suffix = "USDT"

    # Build the trading pair symbol
    symbol = base_symbol + pair_suffix

    await update.message.reply_text(f"🔍 Fetching long/short ratio for {symbol}...")

    ratio_data = await crypto_service.get_long_short_ratio(symbol)

    if ratio_data:
        long_pct = ratio_data["long_percentage"]
        short_pct = ratio_data["short_percentage"]

        # Create visual bar
        bar_length = 20
        long_bars = int((long_pct / 100) * bar_length)
        short_bars = bar_length - long_bars
        visual_bar = "🟢" * long_bars + "🔴" * short_bars

        ratio_text = (
            f"📊 *Long/Short Ratio - {symbol}*\n\n"
            f"Ratio: `{ratio_data['long_short_ratio']:.2f}`\n\n"
            f"{visual_bar}\n"
            f"🟢 Long: `{long_pct:.1f}%`\n"
            f"🔴 Short: `{short_pct:.1f}%`\n\n"
            f"{'📈 More traders are LONG' if long_pct > 50 else '📉 More traders are SHORT'}"
        )
        await update.message.reply_text(ratio_text, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            f"❌ Could not fetch ratio for {symbol}. Try a valid trading pair (e.g., BTCUSDT)."
        )


async def trending_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get trending cryptocurrencies."""
    user = update.effective_user
    await db.log_command(str(user.id), "/trending")

    await update.message.reply_text("🔍 Fetching trending cryptocurrencies...")

    trending = await crypto_service.get_trending_coins()

    if trending:
        trending_text = "🔥 *Trending Cryptocurrencies*\n\n"
        for i, coin in enumerate(trending, 1):
            change = coin.get("price_change_24h")
            change_str = f"`{change:+.2f}%`" if change is not None else "N/A"
            rank = f"#{coin['market_cap_rank']}" if coin.get("market_cap_rank") else "N/A"

            trending_text += (
                f"{i}. *{coin['name']}* ({coin['symbol']})\n"
                f"   Rank: {rank} | 24h: {change_str}\n\n"
            )

        await update.message.reply_text(trending_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Could not fetch trending coins. Please try again later.")


async def sentiment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get market sentiment (Fear & Greed Index)."""
    user = update.effective_user
    await db.log_command(str(user.id), "/sentiment")

    await update.message.reply_text("🔍 Fetching market sentiment...")

    fgi = await crypto_service.get_fear_greed_index()

    if fgi:
        value = fgi["value"]
        classification = fgi["classification"]

        # Emoji based on sentiment
        if value <= 20:
            emoji = "😱"
            sentiment = "Extreme Fear"
        elif value <= 40:
            emoji = "😨"
            sentiment = "Fear"
        elif value <= 60:
            emoji = "😐"
            sentiment = "Neutral"
        elif value <= 80:
            emoji = "😊"
            sentiment = "Greed"
        else:
            emoji = "🤑"
            sentiment = "Extreme Greed"

        # Visual scale
        scale_pos = value // 10
        scale = "▓" * scale_pos + "░" * (10 - scale_pos)

        sentiment_text = (
            f"{emoji} *Crypto Fear & Greed Index*\n\n"
            f"Value: `{value}/100`\n"
            f"Classification: *{classification}*\n"
        )
        
        # Add source info if calculated from market data
        if fgi.get("source") == "market_calculation":
            sentiment_text += (
                f"\n📊 *Market Data:*\n"
                f"• BTC 24h: `{fgi.get('btc_change_24h', 0):+.2f}%`\n"
                f"• Top 10 Avg: `{fgi.get('market_avg_change_24h', 0):+.2f}%`\n"
                f"• Source: Real-time market calculation\n"
            )
        else:
            sentiment_text += f"• Source: Alternative.me\n"
        
        sentiment_text += (
            f"\n0 {scale} 100\n"
            f"😱 Extreme Fear     🤑 Extreme Greed\n\n"
            f"{'📉 Market is fearful - might be a buying opportunity' if value < 50 else '📈 Market is greedy - be cautious of potential correction'}"
        )
        await update.message.reply_text(sentiment_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Could not fetch market sentiment. Please try again later.")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Exception while handling an update: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred. Please try again later."
        )


def main():
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        return

    # Create the Application
    app = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("top", top_command))
    app.add_handler(CommandHandler("details", details_command))
    app.add_handler(CommandHandler("ratio", ratio_command))
    app.add_handler(CommandHandler("trending", trending_command))
    app.add_handler(CommandHandler("sentiment", sentiment_command))
    
    # Register text message handler (for default coin price lookup)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Register error handler
    app.add_error_handler(error_handler)

    # Start the bot
    logger.info("🤖 Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
