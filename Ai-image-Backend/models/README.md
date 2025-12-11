# Models Layer - Database Documentation

## Overview

The models layer handles all database operations and schema definitions for the application.

## Files

### `database.py`
MongoDB connection manager and database operations.

**Key Components:**
- `Database` class - Connection management
- `db` instance - Global database connection

**Methods:**
- `connect()` - Initialize MongoDB connection
- `get_collection()` - Get the ads collection
- `create_indexes()` - Create performance indexes
- `get_stats()` - Get database statistics

### `schema.py`
Complete database schema documentation and validation.

**Key Components:**
- `AdDocumentSchema` - Main document structure
- `ParamsSchema` - Generation parameters structure
- `ImageSchema` - Image object structure
- `EXAMPLE_AD_DOCUMENT` - Example document
- `FIELD_CONSTRAINTS` - Field validation rules
- `COMMON_QUERIES` - Frequently used queries
- `AGGREGATION_PIPELINES` - Complex query examples

**Functions:**
- `create_indexes(db)` - Create recommended indexes
- `validate_ad_document(doc)` - Validate document structure

## Database Structure

### Database Information
- **Database Name**: `ad_generator_db` (configurable via `.env`)
- **Collection**: `generated_ads`
- **Connection**: MongoDB (local or cloud)

### Document Schema

```python
{
    "_id": ObjectId,                    # Auto-generated
    "workspace_id": str,                # Workspace identifier
    "prompt": str,                      # Generation prompt
    "params": {                         # Generation parameters
        "category": str,                # Ad category
        "product_name": str,            # Product name
        "brand_name": str,              # Brand name
        "headline": str,                # Main headline
        "subheadline": str,             # Secondary headline
        "body_copy": str,               # Description
        "price": str,                   # Price
        "original_price": str,          # Original price
        "discount_text": str,           # Discount offer
        "feature_list": [str],          # Features
        "phone": str,                   # Phone number
        "email": str,                   # Email
        "website": str,                 # Website
        "location": str,                # Location
        "cta_text": str,                # Call to action
        "color_theme": str,             # Color theme
        "aspect_ratio": str,            # Required: aspect ratio
        # ... more fields
    },
    "images": [                         # Generated images
        {
            "filename": str,            # Image filename
            "url": str,                 # Full URL
            "type": str                 # "url" or "base64"
        }
    ],
    "mode": str,                        # "custom" or "template"
    "size": str,                        # e.g., "1024x1024"
    "created_at": datetime,             # Creation time (UTC)
    "updated_at": datetime              # Update time (UTC)
}
```

## Usage Examples

### Connect to Database

```python
from models.database import db

# Connect
db.connect()

# Get collection
collection = db.get_collection()
```

### Query Documents

```python
# Get all ads for a workspace
ads = collection.find({"workspace_id": "default"})

# Get ads by category
mobile_ads = collection.find({
    "workspace_id": "default",
    "params.category": "Mobile"
})

# Get recent ads
recent_ads = collection.find(
    {"workspace_id": "default"}
).sort("created_at", -1).limit(10)
```

### Insert Document

```python
from datetime import datetime, timezone

ad_document = {
    "workspace_id": "default",
    "prompt": "Professional ad for iPhone...",
    "params": {
        "category": "Mobile",
        "product_name": "iPhone 15 Pro",
        "headline": "TITANIUM STRONG",
        "aspect_ratio": "instagram_post"
    },
    "images": [
        {
            "filename": "image1.png",
            "url": "http://localhost:5000/images/image1.png",
            "type": "url"
        }
    ],
    "mode": "custom",
    "size": "1024x1024",
    "created_at": datetime.now(timezone.utc),
    "updated_at": datetime.now(timezone.utc)
}

result = collection.insert_one(ad_document)
print(f"Inserted ID: {result.inserted_id}")
```

### Update Document

```python
from bson import ObjectId

collection.update_one(
    {"_id": ObjectId("507f1f77bcf86cd799439011")},
    {"$set": {
        "updated_at": datetime.now(timezone.utc),
        "custom_note": "Updated note"
    }}
)
```

### Delete Document

```python
collection.delete_one({"_id": ObjectId("507f1f77bcf86cd799439011")})
```

### Aggregation

```python
# Count images by workspace
pipeline = [
    {"$match": {"workspace_id": "default"}},
    {"$unwind": "$images"},
    {"$count": "total_images"}
]

result = list(collection.aggregate(pipeline))
total_images = result[0]["total_images"] if result else 0
```

## Indexes

### Recommended Indexes

```python
# Create indexes for better performance
db.create_indexes()
```

**Indexes Created:**
1. `workspace_id + created_at` - Query by workspace, sort by date
2. `workspace_id + params.aspect_ratio` - Filter by aspect ratio
3. `workspace_id + params.category` - Filter by category
4. `created_at` - Sort all by date

## Validation

### Validate Document

```python
from models.schema import validate_ad_document

is_valid, error_msg = validate_ad_document(ad_document)

if is_valid:
    collection.insert_one(ad_document)
else:
    print(f"Validation error: {error_msg}")
```

## Field Constraints

### Required Fields
- `workspace_id` (string)
- `prompt` (string, max 5000 chars)
- `params.aspect_ratio` (string, must be valid ratio)
- `images` (array, min 1 item)
- `mode` (string: "custom" or "template")
- `size` (string: "WIDTHxHEIGHT")
- `created_at` (datetime)
- `updated_at` (datetime)

### Aspect Ratio Values
- `instagram_post` - 1:1 (1024x1024)
- `instagram_story` - 9:16 (1024x1792)
- `facebook_post` - 1:1 (1024x1024)
- `linkedin_post` - 1:1 (1024x1024)
- `pinterest` - 2:3 (1024x1792)
- `twitter_post` - 16:9 (1792x1024)
- `youtube_thumbnail` - 16:9 (1792x1024)
- `wide_banner` - 16:9 (1792x1024)

## Common Queries

See `schema.py` for complete list of common queries and aggregation pipelines.

### Get All Ads by Workspace
```python
ads = collection.find({"workspace_id": "default"}).sort("created_at", -1)
```

### Get Ads by Category
```python
ads = collection.find({
    "workspace_id": "default",
    "params.category": "Mobile"
})
```

### Count Total Ads
```python
count = collection.count_documents({"workspace_id": "default"})
```

### Get All Workspaces
```python
workspaces = collection.distinct("workspace_id")
```

## Statistics

### Get Database Stats

```python
stats = db.get_stats()
print(f"Total documents: {stats['total_documents']}")
print(f"Total workspaces: {stats['total_workspaces']}")
print(f"Workspaces: {stats['workspaces']}")
```

## Best Practices

1. **Always use UTC timestamps** for `created_at` and `updated_at`
2. **Validate documents** before insertion
3. **Create indexes** for frequently queried fields
4. **Use aggregation pipelines** for complex queries
5. **Handle ObjectId conversion** when serializing to JSON
6. **Check collection exists** before operations
7. **Use workspace_id** for multi-tenancy

## Error Handling

```python
try:
    result = collection.insert_one(document)
    print(f"Success: {result.inserted_id}")
except Exception as e:
    print(f"Error: {e}")
```

## Performance Tips

1. Use indexes for frequently queried fields
2. Limit results with `.limit()`
3. Use projection to return only needed fields
4. Use aggregation for complex queries
5. Create compound indexes for multi-field queries

## Migration

If you need to migrate data or change schema:

1. Create migration script
2. Test on development database
3. Backup production database
4. Run migration
5. Verify data integrity

## Monitoring

Monitor database performance:
- Query execution time
- Index usage
- Collection size
- Document count
- Connection pool status

## Backup

Regular backup recommendations:
- Daily automated backups
- Keep 7 days of backups
- Test restore procedures
- Store backups securely

## See Also

- `schema.py` - Complete schema documentation
- `database.py` - Database connection code
- MongoDB documentation: https://docs.mongodb.com/
