"""
Token Cleanup Utility
Cleans up expired blacklisted tokens from the database
This should be run periodically as a cron job
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent
load_dotenv(ROOT_DIR / '.env')

async def cleanup_expired_tokens():
    """Remove expired blacklisted tokens from database"""
    # Database connection
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'ecommerce_db')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        current_time = datetime.now(timezone.utc)
        result = await db.blacklisted_tokens.delete_many({"expires_at": {"$lt": current_time}})
        
        print(f"Cleanup completed: {result.deleted_count} expired tokens removed")
        
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(cleanup_expired_tokens())
