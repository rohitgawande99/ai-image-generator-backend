"""
Configuration settings for the application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory
backend_dir = Path(__file__).parent.parent
dotenv_path = backend_dir / '.env'
load_dotenv(dotenv_path)


class Config:
    """Application configuration"""
    
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("DB_NAME", "ad_generator_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "generated_ads")
    
    # Google Cloud Vertex AI Configuration (for paid users)
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "leadmasters-480212")
    GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "leadmasters-480212-1cab02cbb5cf.json")
    
    # Azure FLUX Configuration (for free users)
    AZURE_FLUX_API_KEY = os.getenv("AZURE_FLUX_API_KEY")
    AZURE_FLUX_ENDPOINT = os.getenv("AZURE_FLUX_ENDPOINT")
    
    # Claude Configuration
    CLAUDE_API_KEY = os.getenv("AZURE_CLAUDE_API_KEY")
    CLAUDE_ENDPOINT = os.getenv("AZURE_CLAUDE_ENDPOINT")
    CLAUDE_DEPLOYMENT = os.getenv("CLAUDE_DEPLOYMENT_NAME", "claude-opus-4-1")
    
    # File Storage
    # Use absolute path relative to this config file's location
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "generated_images")
    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
    
    # Azure Blob Storage Configuration
    AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    AZURE_STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "generated-images")
    
    # Workspace Configuration
    WORKSPACE_ID = os.getenv("WORKSPACE_ID", "default")
    
    # Flask Configuration
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    @classmethod
    def init_app(cls):
        """Initialize application directories"""
        # Create directories relative to backend folder
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.join(backend_dir, 'templates'), exist_ok=True)
        os.makedirs(os.path.join(backend_dir, 'static'), exist_ok=True)
        
        print(f"📁 Upload folder: {cls.UPLOAD_FOLDER}")
        print(f"🆔 Workspace ID configured: '{cls.WORKSPACE_ID}'")
        print(f"🆔 Loaded from .env: {os.getenv('WORKSPACE_ID') is not None}")
