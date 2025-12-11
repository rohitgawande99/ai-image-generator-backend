"""
API routes definition
"""
from flask import Blueprint, jsonify
from config.config import Config
from controllers import (
    config_controller,
    ai_controller,
    prompt_controller,
    image_controller,
    gallery_controller
)

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


# Configuration routes
api_bp.route('/config', methods=['GET'])(config_controller.get_config)
api_bp.route('/health', methods=['GET'])(config_controller.health_check)

# AI routes
api_bp.route('/analyze-image', methods=['POST'])(ai_controller.analyze_image)
api_bp.route('/autofill-fields', methods=['POST'])(ai_controller.autofill_fields)

# Prompt generation routes
api_bp.route('/generate-prompts', methods=['POST'])(prompt_controller.generate_prompts)

# Image generation routes
api_bp.route('/generate-images', methods=['POST'])(image_controller.generate_images)

# Gallery CRUD routes
api_bp.route('/save-to-gallery', methods=['POST'])(gallery_controller.save_to_gallery)
api_bp.route('/ads', methods=['GET'])(gallery_controller.get_all_ads)
api_bp.route('/ads/<ad_id>', methods=['GET'])(gallery_controller.get_ad_by_id)
api_bp.route('/ads/<ad_id>', methods=['PUT'])(gallery_controller.update_ad)
api_bp.route('/ads/<ad_id>', methods=['DELETE'])(gallery_controller.delete_ad)
api_bp.route('/ads/<ad_id>/images/<filename>', methods=['DELETE'])(gallery_controller.delete_image_from_ad)
api_bp.route('/delete-all-ads', methods=['DELETE'])(gallery_controller.delete_all_ads)

# Test endpoint
@api_bp.route('/test', methods=['GET'])
def test():
    print("🧪 TEST ENDPOINT CALLED!")
    return {"test": "working", "workspace": Config.WORKSPACE_ID}
