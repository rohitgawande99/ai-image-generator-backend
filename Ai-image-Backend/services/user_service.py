"""
User service for managing user types and subscriptions
"""
from models.database import db
from datetime import datetime


class UserService:
    """Service for user-related operations"""
    
    def __init__(self):
        # Get users collection directly from db
        if db.db is not None:
            self.users_collection = db.db["users"]
        else:
            self.users_collection = None
    
    def is_paid_user(self, user_id):
        """Check if user is a paid subscriber"""
        if not user_id:
            return False
        
        user = self.users_collection.find_one({"user_id": user_id})
        
        if not user:
            return False
        
        return user.get("is_paid", False)
    
    def get_user(self, user_id):
        """Get user details"""
        return self.users_collection.find_one({"user_id": user_id})
    
    def create_user(self, user_id, email=None, is_paid=False):
        """Create a new user"""
        user_data = {
            "user_id": user_id,
            "email": email,
            "is_paid": is_paid,
            "created_at": datetime.utcnow()
        }
        
        result = self.users_collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def update_user_subscription(self, user_id, is_paid):
        """Update user subscription status"""
        result = self.users_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_paid": is_paid,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    def get_or_create_user(self, user_id, email=None):
        """Get existing user or create new one"""
        user = self.get_user(user_id)
        
        if not user:
            self.create_user(user_id, email, is_paid=False)
            user = self.get_user(user_id)
        
        return user


# Global user service instance
user_service = UserService()
