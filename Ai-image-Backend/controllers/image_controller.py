"""
Image generation controller
"""
from flask import request, jsonify
from config.config import Config
from services.user_service import user_service


def generate_images():
    """Generate images from selected prompt"""
    try:
        # Import image_service inside the function to ensure it's initialized
        from services.image_service import image_service
        
        data = request.get_json()
        
        workspace_id = Config.WORKSPACE_ID
        selected_prompt = data.get("selected_prompt")
        params = data.get("params", {})
        num_images = data.get("num_images", 3)
        
        # Get model selection from frontend (params.image_model)
        # 'free' = Azure FLUX, 'paid' = Gemini 2.5 Flash Image
        image_model = params.get("image_model", "free")
        is_paid_user = (image_model == "paid")
        
        model_name = "Gemini 2.5 Flash Image (Premium)" if is_paid_user else "Azure FLUX (Free)"
        print(f"  🔧 Using model from frontend: {model_name}")
        
        if not selected_prompt:
            return jsonify({"error": "selected_prompt is required"}), 400
        

        
        if image_service is None:
            return jsonify({"error": "Image service not initialized. Please restart the server."}), 500
        
        result = image_service.generate_images(selected_prompt, params, num_images, is_paid_user)
        
        return jsonify({
            "success": True,
            "workspace_id": workspace_id,
            "total_images": result["total"],
            "images": result["images"],
            "prompt": selected_prompt,
            "params": params,
            "size": result["size"],
            "message": f"Generated {result['total']} images successfully"
        }), 201
    
    except Exception as e:
        print(f"❌ Error in generate_images: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
