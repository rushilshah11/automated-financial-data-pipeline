import os
import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.service.email_service import EmailService

# Load variables from the .env file
load_dotenv()  

# Get the database URL from environment variables
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("SQLALCHEMY_DATABASE_URL not set in environment")

# Configure logging to see output in the terminal
logging.basicConfig(level=logging.INFO)

# Create a SQLAlchemy session
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

if __name__ == "__main__":
    asyncio.run(main())