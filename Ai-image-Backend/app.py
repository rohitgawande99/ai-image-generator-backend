"""
Flask Web Application for Social Media Ad Generator
Refactored with MVC architecture
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from config.config import Config
from models.database import db
from routes import api_bp


def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Configure CORS to allow frontend access
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://localhost:5000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        },
        r"/images/*": {
            "origins": ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://localhost:5000"],
            "methods": ["GET"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True
        }
    })
    
    # Initialize configuration
    Config.init_app()
    
    # Initialize database
    db.connect()
    
    # Initialize repositories
    from controllers import gallery_controller
    gallery_controller.init_repository()
    
    # Initialize Azure Storage service
    from services.azure_storage_service import azure_storage_service
    if azure_storage_service.is_available():
        print(f"✅ Azure Blob Storage: ENABLED")
        print(f"   Container: {Config.AZURE_STORAGE_CONTAINER_NAME}")
    else:
        print(f"⚠️  Azure Blob Storage: DISABLED (using local storage)")
    
    # Initialize image service with Google GenAI client
    from services.ai_service import ai_service
    from services import image_service as image_service_module
    from services.image_service import ImageService
    
    # Set the global image_service instance
    print(f"🔧 Initializing image_service with GenAI client: {ai_service.genai_client}")
    image_service_module.image_service = ImageService(ai_service.genai_client, ai_service.image_model_name)
    print(f"✅ image_service initialized: {image_service_module.image_service}")
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Route to serve generated images
    @app.route('/images/<path:filename>')
    def serve_image(filename):
        """Serve generated images from the upload folder"""
        return send_from_directory(Config.UPLOAD_FOLDER, filename)
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*70)
    print("🚀 SOCIAL MEDIA AD GENERATOR - WEB APPLICATION")
    print("="*70)
    print(f"📁 Image storage: {Config.UPLOAD_FOLDER}")
    print(f"🌐 Server URL: {Config.BASE_URL}")
    print(f"💾 MongoDB: {Config.DB_NAME}.{Config.COLLECTION_NAME}")
    print(f"🎨 Frontend: http://localhost:5000")
    print(f"📊 Gallery: http://localhost:5000/gallery")
    print("="*70)
    print("🤖 IMAGE MODEL: User-selectable from frontend")
    print("   • Azure FLUX (Free)")
    print("   • Gemini 2.5 Flash Image (Premium)")
    print("="*70)
    print("="*70 + "\n")
    
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
