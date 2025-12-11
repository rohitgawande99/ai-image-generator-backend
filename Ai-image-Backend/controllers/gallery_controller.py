"""
Gallery CRUD operations controller
"""
from flask import request, jsonify
from repositories.ad_repository import AdRepository
from models.database import db
from utils.serializers import serialize_doc
from utils.image_utils import delete_image_file
from config.config import Config

# Initialize repository
ad_repository = None

def init_repository():
    """Initialize ad repository with database collection"""
    global ad_repository
    collection = db.get_collection()
    if collection is not None:
        ad_repository = AdRepository(collection)
        print("✅ Ad repository initialized")
    else:
        print("⚠️  Ad repository not initialized - database not available")


def save_to_gallery():
    """Save specific images to gallery"""
    try:
        if ad_repository is None:
            return jsonify({"error": "Repository not initialized"}), 500
        
        data = request.get_json()
        
        workspace_id = data.get("workspace_id", Config.WORKSPACE_ID)
        selected_prompt = data.get("prompt", "")
        params = data.get("params", {})
        images = data.get("images", [])
        size = data.get("size", "1024x1024")
        
        if not images or len(images) == 0:
            return jsonify({"error": "No images provided"}), 400
        
        print(f"\n💾 Saving {len(images)} images to gallery...")
        
        ad_id = ad_repository.create_ad(
            workspace_id=workspace_id,
            prompt=selected_prompt,
            params=params,
            images=images,
            size=size,
            mode="custom"
        )
        
        if not ad_id:
            return jsonify({"error": "Failed to save to gallery"}), 500
        
        print(f"  ✅ Saved to gallery with ID: {ad_id}")
        
        return jsonify({
            "success": True,
            "ad_id": ad_id,
            "message": f"Saved {len(images)} images to gallery"
        }), 201
        
    except Exception as e:
        print(f"❌ Error saving to gallery: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def get_all_ads():
    """Get all ads from workspace"""
    try:
        if ad_repository is None:
            return jsonify({"error": "Repository not initialized"}), 500
        
        print("\n" + "="*50)
        print("🔍 GET_ALL_ADS CALLED")
        print("="*50)
        
        workspace_id = Config.WORKSPACE_ID
        print(f"📋 Config.WORKSPACE_ID: '{workspace_id}'")
        
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        aspect_ratio = request.args.get('aspect_ratio')
        
        print(f"🔍 Querying MongoDB...")
        
        ads, total = ad_repository.get_ads_by_workspace(
            workspace_id=workspace_id,
            skip=skip,
            limit=limit,
            aspect_ratio=aspect_ratio
        )
        
        print(f"✅ Found {total} ads, returning {len(ads)} ads")
        print("="*50 + "\n")
        
        serialized_ads = [serialize_doc(ad) for ad in ads]
        
        return jsonify({
            "success": True,
            "total": total,
            "count": len(serialized_ads),
            "ads": serialized_ads
        }), 200
    
    except Exception as e:
        print(f"❌ ERROR in get_all_ads: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def get_ad_by_id(ad_id):
    """Get specific ad by ID"""
    try:
        if ad_repository is None:
            return jsonify({"error": "Repository not initialized"}), 500
        
        ad = ad_repository.get_ad_by_id(ad_id)
        
        if not ad:
            return jsonify({"error": "Ad not found"}), 404
        
        return jsonify({
            "success": True,
            "ad": serialize_doc(ad)
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_ad(ad_id):
    """Update ad metadata"""
    try:
        if ad_repository is None:
            return jsonify({"error": "Repository not initialized"}), 500
        
        data = request.get_json()
        
        success = ad_repository.update_ad_metadata(
            ad_id=ad_id,
            params=data.get("params"),
            custom_note=data.get("custom_note"),
            tags=data.get("tags")
        )
        
        if not success:
            return jsonify({"error": "Ad not found or update failed"}), 404
        
        updated_ad = ad_repository.get_ad_by_id(ad_id)
        
        return jsonify({
            "success": True,
            "message": "Ad updated successfully",
            "ad": serialize_doc(updated_ad)
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_image_from_ad(ad_id, filename):
    """Delete specific image from an ad"""
    try:
        if ad_repository is None:
            return jsonify({"error": "Repository not initialized"}), 500
        
        updated_images = ad_repository.remove_image_from_ad(ad_id, filename)
        
        if updated_images is None:
            return jsonify({"error": "Ad not found or update failed"}), 404
        
        delete_image_file(filename)
        
        return jsonify({
            "success": True,
            "message": f"Image {filename} deleted successfully",
            "remaining_images": len(updated_images)
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_ad(ad_id):
    """Delete entire ad and all associated images"""
    try:
        if ad_repository is None:
            return jsonify({"error": "Repository not initialized"}), 500
        
        ad = ad_repository.delete_ad(ad_id)
        
        if not ad:
            return jsonify({"error": "Ad not found"}), 404
        
        deleted_files = 0
        for image in ad.get("images", []):
            if delete_image_file(image["filename"]):
                deleted_files += 1
        
        return jsonify({
            "success": True,
            "message": "Ad deleted successfully",
            "deleted_files": deleted_files
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_all_ads():
    """Delete all ads from the gallery"""
    try:
        if ad_repository is None:
            return jsonify({"error": "Repository not initialized"}), 500
        
        workspace_id = Config.WORKSPACE_ID
        
        print(f"\n🗑️  Deleting all ads for workspace: {workspace_id}")
        
        deleted_count = ad_repository.delete_ads_by_workspace(workspace_id)
        
        print(f"  ✅ Deleted {deleted_count} ads")
        
        return jsonify({
            "success": True,
            "deleted_count": deleted_count,
            "message": f"Deleted {deleted_count} ads from gallery"
        }), 200
        
    except Exception as e:
        print(f"❌ Error deleting ads: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def get_stats():
    """Get overall statistics"""
    try:
        if ad_repository is None:
            return jsonify({"error": "Repository not initialized"}), 500
        
        workspace_id = Config.WORKSPACE_ID
        stats = ad_repository.get_workspace_stats(workspace_id)
        
        all_workspaces = ad_repository.get_all_workspaces()
        
        return jsonify({
            "success": True,
            "total_ads": stats["total_ads"],
            "total_images": stats["total_images"],
            "total_workspaces": len(all_workspaces),
            "workspaces": all_workspaces
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def debug_workspaces():
    """Debug: List all workspace_ids in database"""
    try:
        if ad_repository is None:
            return jsonify({"error": "Repository not initialized"}), 500
        
        all_workspaces = ad_repository.get_all_workspaces()
        workspace_counts = ad_repository.get_workspace_counts()
        
        current_workspace = Config.WORKSPACE_ID
        current_count = workspace_counts.get(current_workspace, 0)
        
        total_docs = sum(workspace_counts.values())
        
        return jsonify({
            "success": True,
            "configured_workspace_id": current_workspace,
            "configured_workspace_count": current_count,
            "all_workspaces": all_workspaces,
            "workspace_counts": workspace_counts,
            "total_documents": total_docs
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
