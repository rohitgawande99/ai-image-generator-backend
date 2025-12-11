"""
AI operations controller
"""
from flask import request, jsonify
from services.ai_service import ai_service


def analyze_image():
    """Analyze uploaded image with Claude Vision"""
    try:
        data = request.get_json()
        uploaded_image_base64 = data.get("image", "")
        
        if not uploaded_image_base64:
            return jsonify({"error": "Image data is required"}), 400
        
        analysis_data = ai_service.analyze_image_for_extraction(uploaded_image_base64)
        
        return jsonify({
            "success": True,
            "visual_description": analysis_data.get("visual_description", ""),
            "extracted_fields": analysis_data
        }), 200
        
    except Exception as e:
        print(f"❌ Error in analyze_image: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def autofill_fields():
    """Use Claude AI to auto-fill form fields"""
    try:
        data = request.get_json()
        
        product_description = data.get("product_description", "")
        category = data.get("category", "")
        brand_name = data.get("brand_name", "")
        
        if not product_description:
            return jsonify({"error": "Product description is required"}), 400
        
        autofill_data = ai_service.autofill_fields_with_ai(
            product_description, 
            category, 
            brand_name
        )
        
        return jsonify({
            "success": True,
            "data": autofill_data
        }), 200
        
    except Exception as e:
        print(f"❌ Error in autofill_fields: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
