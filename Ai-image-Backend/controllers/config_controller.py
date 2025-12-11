"""
Configuration controller
"""
from flask import jsonify
from services.ai_service import ai_service
from config.config import Config


def get_config():
    """Get configuration options for frontend"""
    config_options = ai_service.get_config_options()
    config_options["workspace_id"] = Config.WORKSPACE_ID
    
    return jsonify({
        "success": True,
        **config_options
    })


def health_check():
    """Health check endpoint"""
    from datetime import datetime, timezone
    return jsonify({
        "status": "healthy",
        "mongodb": "connected" if Config else "disconnected",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
