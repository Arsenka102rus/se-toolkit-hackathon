"""Database helper for bot - uses backend API to interact with database"""
import os
import httpx
from datetime import datetime


class BotDatabase:
    """Database operations for the Telegram bot using backend API"""

    def __init__(self):
        self.api_url = os.getenv("API_URL", "http://127.0.0.1:8000")

    async def register_user(self, telegram_id: str, username: str = None,
                           first_name: str = None, last_name: str = None) -> bool:
        """Register or update user in database"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/users/",
                    json={
                        "telegram_id": telegram_id,
                        "username": username,
                        "first_name": first_name,
                        "last_name": last_name,
                    },
                    timeout=5.0,
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Error registering user: {e}")
            return False

    async def get_user_stats(self, telegram_id: str) -> dict:
        """Get user statistics"""
        # For now, return basic info - can be extended with more API endpoints
        return {
            "telegram_id": telegram_id,
            "registered": True,
            "last_active": datetime.now().isoformat(),
        }

    async def log_command(self, telegram_id: str, command: str) -> bool:
        """Log user command usage"""
        # Could add a dedicated API endpoint for this
        print(f"User {telegram_id} ran command: {command}")
        return True


# Singleton instance
db = BotDatabase()
