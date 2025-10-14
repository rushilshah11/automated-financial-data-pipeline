import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv() 

# Pydantic's BaseSettings handles reading environment variables for us
class Settings(BaseSettings):
    # This URL will read the value directly from the .env file or OS environment
    SQLALCHEMY_DATABASE_URL: str 
    
    # You can also define other keys you need
    FINNHUB_API_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str 
    
    EMAIL_FROM_ADDRESS: str 

    S3_BUCKET_NAME: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str

    # Pydantic setting to specify where to read environment variables from
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


# Create the final settings instance
settings = Settings()

# Example of accessing the variable:
# print(settings.SQLALCHEMY_DATABASE_URL)