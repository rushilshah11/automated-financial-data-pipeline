import os
import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime, timedelta


from app.service.email_service import EmailService

# Load env vars
load_dotenv()

DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("SQLALCHEMY_DATABASE_URL not set in environment")

# Logging
logging.basicConfig(level=logging.INFO)

# SQLAlchemy session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

async def main():
    session = SessionLocal()
    try:
        email_service = EmailService(session=session)
        sent_count = await email_service.dispatch_daily_updates()
        print(f"Emails sent: {sent_count}")
    finally:
        session.close()

async def periodic_dispatch():
    
    # while True:
    #     now = datetime.now()
    #     target = now.replace(hour=19, minute=50, second=0, microsecond=0)
    #     if now >= target:
    #         target += timedelta(days=1)

    #     sleep_seconds = (target - now).total_seconds()
    #     logging.info(f"Sleeping for {sleep_seconds} seconds until next dispatch")
    #     await asyncio.sleep(sleep_seconds)

        # Run dispatch
        await main()

if __name__ == "__main__":
    asyncio.run(periodic_dispatch())