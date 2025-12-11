"""
Ad repository for managing generated ads in MongoDB
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from bson import ObjectId

from .base_repository import BaseRepository


class AdRepository(BaseRepository):
    """Repository for ad/image generation operations"""
    
    def get_collection_name(self) -> str:
        """Get the collection name"""
        return "generated_ads"
    
    def create_ad(
        self,
        workspace_id: str,
        prompt: str,
        params: Dict[str, Any],
        images: List[Dict[str, str]],
        size: str,
        mode: str = "custom"
    ) -> Optional[str]:
        """
        Create new ad document
        
        Args:
            workspace_id: Workspace identifier
            prompt: Generation prompt
            params: Generation parameters
            images: List of image dicts with filename, url, type
            size: Image size (e.g., "1024x1024")
            mode: Generation mode ("custom" or "template")
            
        Returns:
            Created ad ID or None if failed
        """
        ad_document = {
            "workspace_id": workspace_id,
            "prompt": prompt,
            "params": params,
            "images": images,
            "mode": mode,
            "size": size,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        return self.insert_one(ad_document)
    
    def get_ad_by_id(self, ad_id: str) -> Optional[Dict[str, Any]]:
        """
        Get ad by ID
        
        Args:
            ad_id: Ad document ID
            
        Returns:
            Ad document or None if not found
        """
        return self.find_by_id(ad_id)
    
    def get_ads_by_workspace(
        self,
        workspace_id: str,
        skip: int = 0,
        limit: int = 50,
        aspect_ratio: Optional[str] = None
    ) -> tuple[List[Dict[str, Any]], int]:
        """
        Get ads for a workspace with pagination
        
        Args:
            workspace_id: Workspace identifier
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            aspect_ratio: Optional aspect ratio filter
            
        Returns:
            Tuple of (ads list, total count)
        """
        query = {"workspace_id": workspace_id}
        
        if aspect_ratio:
            query["params.aspect_ratio"] = aspect_ratio
        
        ads = self.find_many(
            query=query,
            skip=skip,
            limit=limit,
            sort=[("created_at", -1)]
        )
        
        total = self.count(query)
        
        return ads, total
    
    def update_ad_metadata(
        self,
        ad_id: str,
        params: Optional[Dict[str, Any]] = None,
        custom_note: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """
        Update ad metadata
        
        Args:
            ad_id: Ad document ID
            params: Optional updated parameters
            custom_note: Optional custom note
            tags: Optional tags list
            
        Returns:
            True if updated, False otherwise
        """
        update_doc = {
            "updated_at": datetime.now(timezone.utc)
        }
        
        if params is not None:
            update_doc["params"] = params
        if custom_note is not None:
            update_doc["custom_note"] = custom_note
        if tags is not None:
            update_doc["tags"] = tags
        
        return self.update_by_id(ad_id, {"$set": update_doc})
    
    def remove_image_from_ad(
        self,
        ad_id: str,
        filename: str
    ) -> Optional[List[Dict[str, str]]]:
        """
        Remove specific image from ad
        
        Args:
            ad_id: Ad document ID
            filename: Image filename to remove
            
        Returns:
            Updated images list or None if failed
        """
        ad = self.get_ad_by_id(ad_id)
        if not ad:
            return None
        
        updated_images = [
            img for img in ad.get("images", [])
            if img["filename"] != filename
        ]
        
        success = self.update_by_id(
            ad_id,
            {
                "$set": {
                    "images": updated_images,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        
        return updated_images if success else None
    
    def delete_ad(self, ad_id: str) -> Optional[Dict[str, Any]]:
        """
        Delete ad and return its data for cleanup
        
        Args:
            ad_id: Ad document ID
            
        Returns:
            Deleted ad document or None if not found
        """
        ad = self.get_ad_by_id(ad_id)
        if not ad:
            return None
        
        success = self.delete_by_id(ad_id)
        return ad if success else None
    
    def delete_ads_by_workspace(self, workspace_id: str) -> int:
        """
        Delete all ads for a workspace
        
        Args:
            workspace_id: Workspace identifier
            
        Returns:
            Number of ads deleted
        """
        return self.delete_many({"workspace_id": workspace_id})
    
    def get_workspace_stats(self, workspace_id: str) -> Dict[str, Any]:
        """
        Get statistics for a workspace
        
        Args:
            workspace_id: Workspace identifier
            
        Returns:
            Stats dict with total_ads, total_images, etc.
        """
        query = {"workspace_id": workspace_id}
        
        total_ads = self.count(query)
        
        # Count total images using aggregation
        pipeline = [
            {"$match": query},
            {"$unwind": "$images"},
            {"$count": "total_images"}
        ]
        
        image_count_result = self.aggregate(pipeline)
        total_images = image_count_result[0]["total_images"] if image_count_result else 0
        
        return {
            "total_ads": total_ads,
            "total_images": total_images,
            "workspace_id": workspace_id
        }
    
    def get_all_workspaces(self) -> List[str]:
        """
        Get list of all workspace IDs
        
        Returns:
            List of workspace IDs
        """
        return self.distinct("workspace_id")
    
    def get_global_stats(self) -> Dict[str, Any]:
        """
        Get global statistics across all workspaces
        
        Returns:
            Stats dict with totals and workspace info
        """
        total_ads = self.count({})
        
        # Count total images
        pipeline = [
            {"$unwind": "$images"},
            {"$count": "total_images"}
        ]
        
        image_count_result = self.aggregate(pipeline)
        total_images = image_count_result[0]["total_images"] if image_count_result else 0
        
        workspaces = self.get_all_workspaces()
        
        return {
            "total_ads": total_ads,
            "total_images": total_images,
            "total_workspaces": len(workspaces),
            "workspaces": workspaces
        }
    
    def get_workspace_counts(self) -> Dict[str, int]:
        """
        Get ad count for each workspace
        
        Returns:
            Dict mapping workspace_id to ad count
        """
        workspaces = self.get_all_workspaces()
        
        workspace_counts = {}
        for ws in workspaces:
            count = self.count({"workspace_id": ws})
            workspace_counts[ws] = count
        
        return workspace_counts
