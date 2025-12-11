"""
MongoDB Database Schema Documentation

This file documents the structure of all collections in the database.
MongoDB is schema-less, but this serves as documentation for developers.
"""

from datetime import datetime, timezone
from typing import TypedDict, List, Optional


class ImageSchema(TypedDict):
    """
    Schema for individual image objects stored in ads
    """
    filename: str           # e.g., "default_Mobile_5c134c7b.png"
    url: str               # Azure Blob URL or local URL
                           # Azure: "https://account.blob.core.windows.net/container/file.png?sv=..."
                           # Local: "http://localhost:5000/images/file.png"
    type: str              # "url" or "base64"
    storage: Optional[str]  # "azure" or "local" (added Dec 2025)


class ParamsSchema(TypedDict):
    """
    Schema for generation parameters
    All fields are optional as they depend on user input
    """
    # Basic Info
    category: Optional[str]              # e.g., "Mobile", "Real Estate", "Education"
    product_name: Optional[str]          # e.g., "iPhone 15 Pro"
    brand_name: Optional[str]            # e.g., "Apple"
    
    # Text Content
    headline: Optional[str]              # Main headline text
    subheadline: Optional[str]           # Secondary headline
    body_copy: Optional[str]             # Description text
    tagline: Optional[str]               # Brand tagline
    
    # Pricing
    price: Optional[str]                 # e.g., "$999"
    original_price: Optional[str]        # e.g., "$1,199" (crossed out)
    discount_text: Optional[str]         # e.g., "Save $200"
    offer_label: Optional[str]           # e.g., "SALE", "NEW", "LIMITED"
    
    # Features
    feature_list: Optional[List[str]]    # List of product features
    
    # Contact Information
    contact_info: Optional[str]          # General contact info
    phone: Optional[str]                 # Phone number
    email: Optional[str]                 # Email address
    website: Optional[str]               # Website URL
    location: Optional[str]              # Physical location
    
    # Call to Action
    cta_text: Optional[str]              # e.g., "Buy Now", "Learn More"
    
    # Visual Preferences
    color_theme: Optional[str]           # e.g., "Gold, Navy Blue"
    background_color: Optional[str]      # e.g., "Dark Blue"
    text_color: Optional[str]            # Text color preference
    accent_color: Optional[str]          # Accent color
    
    # Generation Settings
    aspect_ratio: str                    # Required: "instagram_post", "instagram_story", etc.
    image_model: Optional[str]           # "free" (Azure FLUX) or "paid" (Gemini) - added Dec 2025
    num_variations: Optional[int]        # Number of prompt variations (1-3) - added Dec 2025
    
    # Image Upload (if using uploaded image)
    use_uploaded_image: Optional[bool]   # True if user uploaded reference image
    uploaded_image: Optional[str]        # Base64 encoded image data


class AdDocumentSchema(TypedDict):
    """
    Main schema for ad documents in the 'generated_ads' collection
    
    Collection: generated_ads
    Database: ad_generator_db (default)
    """
    _id: str                            # MongoDB ObjectId (auto-generated)
    workspace_id: str                   # Workspace identifier (e.g., "default")
    prompt: str                         # The full prompt used for generation
    params: ParamsSchema                # Generation parameters (see ParamsSchema)
    images: List[ImageSchema]           # List of generated images (see ImageSchema)
    mode: str                           # Generation mode: "custom", "template", etc.
    size: str                           # Image dimensions: "1024x1024", "1024x1792", etc.
    created_at: datetime                # When the ad was created (UTC)
    updated_at: datetime                # When the ad was last updated (UTC)
    
    # Optional fields (may be added by updates)
    custom_note: Optional[str]          # User notes about the ad
    tags: Optional[List[str]]           # User-defined tags for organization


# Example Document (Updated - with Azure Blob Storage)
EXAMPLE_AD_DOCUMENT = {
    "_id": "507f1f77bcf86cd799439011",
    "workspace_id": "default",
    "prompt": "Professional advertising poster for iPhone 15 Pro. Main headline: 'TITANIUM STRONG'. Price: $999. Modern tech aesthetic with studio lighting. Full-bleed edge-to-edge composition with NO frames...",
    "params": {
        "category": "Mobile",
        "product_name": "iPhone 15 Pro",
        "brand_name": "Apple",
        "headline": "TITANIUM STRONG",
        "subheadline": "Pro. Beyond.",
        "price": "$999",
        "original_price": "$1,199",
        "discount_text": "Save $200",
        "feature_list": "• A17 Pro Chip\n• Titanium Design\n• Action Button\n• USB-C",
        "cta_text": "Buy Now",
        "color_theme": "Space Black, Blue",
        "background_color": "Dark gradient",
        "aspect_ratio": "instagram_post",
        "image_model": "free",  # NEW: Model selection
        "num_variations": 3     # NEW: Prompt variations
    },
    "images": [
        {
            "filename": "default_Mobile_5c134c7b.png",
            "url": "https://lmimagegen.blob.core.windows.net/generated-images/default_Mobile_5c134c7b.png?sv=2023-11-03&st=2025-12-10T11%3A27%3A50Z&se=2035-12-10T11%3A27%3A50Z&sr=b&sp=r&sig=abc123...",
            "type": "base64",
            "storage": "azure"  # NEW: Storage location
        },
        {
            "filename": "default_Mobile_730a56f1.png",
            "url": "https://lmimagegen.blob.core.windows.net/generated-images/default_Mobile_730a56f1.png?sv=2023-11-03&st=2025-12-10T11%3A27%3A50Z&se=2035-12-10T11%3A27%3A50Z&sr=b&sp=r&sig=def456...",
            "type": "base64",
            "storage": "azure"
        },
        {
            "filename": "default_Mobile_92aac29c.png",
            "url": "https://lmimagegen.blob.core.windows.net/generated-images/default_Mobile_92aac29c.png?sv=2023-11-03&st=2025-12-10T11%3A27%3A50Z&se=2035-12-10T11%3A27%3A50Z&sr=b&sp=r&sig=ghi789...",
            "type": "base64",
            "storage": "azure"
        }
    ],
    "mode": "custom",
    "size": "1024x1024",
    "created_at": "2025-12-10T10:30:00.000Z",
    "updated_at": "2025-12-10T10:30:00.000Z"
}


# Database Indexes (Recommended)
RECOMMENDED_INDEXES = [
    {
        "collection": "generated_ads",
        "index": {"workspace_id": 1, "created_at": -1},
        "description": "Query ads by workspace, sorted by creation date"
    },
    {
        "collection": "generated_ads",
        "index": {"workspace_id": 1, "params.aspect_ratio": 1},
        "description": "Filter ads by workspace and aspect ratio"
    },
    {
        "collection": "generated_ads",
        "index": {"workspace_id": 1, "params.category": 1},
        "description": "Filter ads by workspace and category"
    },
    {
        "collection": "generated_ads",
        "index": {"created_at": -1},
        "description": "Sort all ads by creation date"
    }
]


# Field Constraints and Validation
FIELD_CONSTRAINTS = {
    "workspace_id": {
        "type": "string",
        "required": True,
        "description": "Identifier for the workspace/user"
    },
    "prompt": {
        "type": "string",
        "required": True,
        "max_length": 5000,
        "description": "Full prompt text used for image generation"
    },
    "params.aspect_ratio": {
        "type": "string",
        "required": True,
        "allowed_values": [
            "instagram_post",      # 1:1 (1024x1024)
            "instagram_story",     # 9:16 (1024x1792)
            "facebook_post",       # 1:1 (1024x1024)
            "linkedin_post",       # 1:1 (1024x1024)
            "pinterest",           # 2:3 (1024x1792)
            "twitter_post",        # 16:9 (1792x1024)
            "youtube_thumbnail",   # 16:9 (1792x1024)
            "wide_banner"          # 16:9 (1792x1024)
        ],
        "description": "Target aspect ratio for generated images"
    },
    "images": {
        "type": "array",
        "required": True,
        "min_items": 1,
        "description": "At least one image must be present"
    },
    "mode": {
        "type": "string",
        "required": True,
        "allowed_values": ["custom", "template"],
        "description": "Generation mode used"
    },
    "size": {
        "type": "string",
        "required": True,
        "pattern": r"^\d+x\d+$",
        "examples": ["1024x1024", "1024x1792", "1792x1024"],
        "description": "Image dimensions in pixels"
    },
    "created_at": {
        "type": "datetime",
        "required": True,
        "description": "UTC timestamp of creation"
    },
    "updated_at": {
        "type": "datetime",
        "required": True,
        "description": "UTC timestamp of last update"
    }
}


# Common Queries
COMMON_QUERIES = {
    "get_all_ads_by_workspace": {
        "query": {"workspace_id": "default"},
        "sort": {"created_at": -1},
        "description": "Get all ads for a workspace, newest first"
    },
    "get_ads_by_category": {
        "query": {
            "workspace_id": "default",
            "params.category": "Mobile"
        },
        "description": "Get all ads in a specific category"
    },
    "get_ads_by_aspect_ratio": {
        "query": {
            "workspace_id": "default",
            "params.aspect_ratio": "instagram_post"
        },
        "description": "Get all ads with specific aspect ratio"
    },
    "get_recent_ads": {
        "query": {"workspace_id": "default"},
        "sort": {"created_at": -1},
        "limit": 10,
        "description": "Get 10 most recent ads"
    },
    "count_ads_by_workspace": {
        "query": {"workspace_id": "default"},
        "operation": "count_documents",
        "description": "Count total ads in workspace"
    },
    "get_all_workspaces": {
        "operation": "distinct",
        "field": "workspace_id",
        "description": "Get list of all workspace IDs"
    }
}


# Aggregation Pipelines
AGGREGATION_PIPELINES = {
    "count_images_by_workspace": [
        {"$match": {"workspace_id": "default"}},
        {"$unwind": "$images"},
        {"$count": "total_images"}
    ],
    "ads_by_category": [
        {"$match": {"workspace_id": "default"}},
        {"$group": {
            "_id": "$params.category",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ],
    "ads_by_aspect_ratio": [
        {"$match": {"workspace_id": "default"}},
        {"$group": {
            "_id": "$params.aspect_ratio",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ],
    "recent_ads_with_image_count": [
        {"$match": {"workspace_id": "default"}},
        {"$addFields": {
            "image_count": {"$size": "$images"}
        }},
        {"$sort": {"created_at": -1}},
        {"$limit": 10}
    ]
}


def create_indexes(db):
    """
    Create recommended indexes on the database
    
    Usage:
        from models.database import db
        from models.schema import create_indexes
        create_indexes(db.db)
    """
    collection = db['generated_ads']
    
    # Create indexes
    collection.create_index([("workspace_id", 1), ("created_at", -1)])
    collection.create_index([("workspace_id", 1), ("params.aspect_ratio", 1)])
    collection.create_index([("workspace_id", 1), ("params.category", 1)])
    collection.create_index([("created_at", -1)])
    
    print("✅ Database indexes created successfully")


def validate_ad_document(doc: dict) -> tuple[bool, str]:
    """
    Validate an ad document against the schema
    
    Args:
        doc: Dictionary representing an ad document
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    required_fields = ['workspace_id', 'prompt', 'params', 'images', 'mode', 'size', 'created_at', 'updated_at']
    
    for field in required_fields:
        if field not in doc:
            return False, f"Missing required field: {field}"
    
    # Check params.aspect_ratio
    if 'aspect_ratio' not in doc.get('params', {}):
        return False, "Missing required field: params.aspect_ratio"
    
    allowed_ratios = FIELD_CONSTRAINTS['params.aspect_ratio']['allowed_values']
    if doc['params']['aspect_ratio'] not in allowed_ratios:
        return False, f"Invalid aspect_ratio. Must be one of: {', '.join(allowed_ratios)}"
    
    # Check images array
    if not isinstance(doc['images'], list) or len(doc['images']) == 0:
        return False, "images must be a non-empty array"
    
    # Validate each image
    for i, img in enumerate(doc['images']):
        if 'filename' not in img or 'url' not in img or 'type' not in img:
            return False, f"Image {i} missing required fields (filename, url, type)"
    
    return True, "Valid"


# Export schema information
__all__ = [
    'ImageSchema',
    'ParamsSchema',
    'AdDocumentSchema',
    'EXAMPLE_AD_DOCUMENT',
    'RECOMMENDED_INDEXES',
    'FIELD_CONSTRAINTS',
    'COMMON_QUERIES',
    'AGGREGATION_PIPELINES',
    'create_indexes',
    'validate_ad_document'
]
