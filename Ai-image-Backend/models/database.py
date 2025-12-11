"""
Database connection and initialization

Database Structure:
-------------------
Database: ad_generator_db (default, configurable via .env)
Collection: generated_ads

Document Schema:
{
    "_id": ObjectId,                    # Auto-generated MongoDB ID
    "workspace_id": str,                # Workspace identifier
    "prompt": str,                      # Full generation prompt
    "params": {                         # Generation parameters
        "category": str,                # e.g., "Mobile", "Real Estate"
        "product_name": str,            # Product/service name
        "brand_name": str,              # Brand name
        "headline": str,                # Main headline
        "subheadline": str,             # Secondary headline
        "price": str,                   # Price text
        "aspect_ratio": str,            # Required: image aspect ratio
        ... (see models/schema.py for complete structure)
    },
    "images": [                         # Array of generated images
        {
            "filename": str,            # Image filename
            "url": str,                 # Full image URL
            "type": str                 # "url" or "base64"
        }
    ],
    "mode": str,                        # "custom" or "template"
    "size": str,                        # e.g., "1024x1024"
    "created_at": datetime,             # Creation timestamp (UTC)
    "updated_at": datetime              # Last update timestamp (UTC)
}

For complete schema documentation, see models/schema.py
"""
from pymongo import MongoClient
from config.config import Config


class Database:
    """
    MongoDB database connection manager
    
    Manages connection to MongoDB and provides access to collections.
    
    Collections:
        - generated_ads: Stores all generated advertising images and metadata
    
    Usage:
        from models.database import db
        
        # Connect to database
        db.connect()
        
        # Get collection
        collection = db.get_collection()
        
        # Query documents
        ads = collection.find({"workspace_id": "default"})
    """
    
    def __init__(self):
        self.client = None
        self.db = None
        self.ads_collection = None
    
    def connect(self):
        """
        Initialize MongoDB connection
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client[Config.DB_NAME]
            self.ads_collection = self.db[Config.COLLECTION_NAME]
            print("✅ MongoDB connected successfully")
            print(f"   Database: {Config.DB_NAME}")
            print(f"   Collection: {Config.COLLECTION_NAME}")
            return True
        except Exception as e:
            print(f"⚠️  MongoDB connection error: {e}")
            return False
    
    def get_collection(self):
        """
        Get ads collection
        
        Returns:
            pymongo.collection.Collection: The generated_ads collection
        """
        return self.ads_collection
    
    def create_indexes(self):
        """
        Create recommended indexes for better query performance
        
        Indexes:
            - workspace_id + created_at (descending)
            - workspace_id + params.aspect_ratio
            - workspace_id + params.category
            - created_at (descending)
        """
        if self.ads_collection is None:
            print("⚠️  Cannot create indexes: Collection not initialized")
            return False
        
        try:
            # Index for querying by workspace and sorting by date
            self.ads_collection.create_index([
                ("workspace_id", 1),
                ("created_at", -1)
            ])
            
            # Index for filtering by aspect ratio
            self.ads_collection.create_index([
                ("workspace_id", 1),
                ("params.aspect_ratio", 1)
            ])
            
            # Index for filtering by category
            self.ads_collection.create_index([
                ("workspace_id", 1),
                ("params.category", 1)
            ])
            
            # Index for sorting by date
            self.ads_collection.create_index([("created_at", -1)])
            
            print("✅ Database indexes created successfully")
            return True
        except Exception as e:
            print(f"⚠️  Error creating indexes: {e}")
            return False
    
    def get_stats(self):
        """
        Get database statistics
        
        Returns:
            dict: Database statistics including document counts
        """
        if self.ads_collection is None:
            return {"error": "Collection not initialized"}
        
        try:
            total_docs = self.ads_collection.count_documents({})
            workspaces = self.ads_collection.distinct("workspace_id")
            
            return {
                "total_documents": total_docs,
                "total_workspaces": len(workspaces),
                "workspaces": workspaces,
                "database": Config.DB_NAME,
                "collection": Config.COLLECTION_NAME
            }
        except Exception as e:
            return {"error": str(e)}


# Global database instance
db = Database()
