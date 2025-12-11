"""
User management controller
"""
from flask import request, jsonify
from services.user_service import user_service


def get_user_status():
    """Get user subscription status"""
    try:
        user_id = request.args.get("user_id", "default")
        
        user = user_service.get_or_create_user(user_id)
        
        return jsonify({
            "success": True,
            "user_id": user["user_id"],
            "is_paid": user.get("is_paid", False),
            "email": user.get("email"),
            "model": "Gemini 2.5 Flash Image" if user.get("is_paid", False) else "Azure FLUX"
        }), 200
    
    except Exception as e:
        print(f"❌ Error in get_user_status: {e}")
        return jsonify({"error": str(e)}), 500


def update_user_subscription():
    """Update user subscription status"""
    try:
        data = request.get_json()
        
        user_id = data.get("user_id")
        is_paid = data.get("is_paid", False)
        
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        # Get or create user
        user = user_service.get_or_create_user(user_id)
        
        # Update subscription
        success = user_service.update_user_subscription(user_id, is_paid)
        
        if success:
            return jsonify({
                "success": True,
                "message": f"User subscription updated to {'paid' if is_paid else 'free'}",
                "user_id": user_id,
                "is_paid": is_paid,
                "model": "Gemini 2.5 Flash Image" if is_paid else "Azure FLUX"
            }), 200
        else:
            return jsonify({"error": "Failed to update subscription"}), 500
    
    except Exception as e:
        print(f"❌ Error in update_user_subscription: {e}")
        return jsonify({"error": str(e)}), 500


def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        user_id = data.get("user_id")
        email = data.get("email")
        is_paid = data.get("is_paid", False)
        
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        # Check if user already exists
        existing_user = user_service.get_user(user_id)
        if existing_user:
            return jsonify({"error": "User already exists"}), 400
        
        # Create user
        user_service.create_user(user_id, email, is_paid)
        
        return jsonify({
            "success": True,
            "message": "User created successfully",
            "user_id": user_id,
            "is_paid": is_paid,
            "model": "Gemini 2.5 Flash Image" if is_paid else "Azure FLUX"
        }), 201
    
    except Exception as e:
        print(f"❌ Error in create_user: {e}")
        return jsonify({"error": str(e)}), 500
