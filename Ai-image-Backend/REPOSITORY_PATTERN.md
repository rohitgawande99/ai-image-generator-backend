# Repository Pattern Implementation

## Overview

The backend has been refactored to implement the **Repository Pattern**, which separates data access logic from business logic. This provides better code organization, testability, and maintainability.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP Requests
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Routes (api_routes.py)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Controllers (gallery_controller.py)             │
│  - Request validation                                        │
│  - Response formatting                                       │
│  - Business logic orchestration                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Repositories (ad_repository.py)                 │
│  - Data access logic                                         │
│  - MongoDB operations                                        │
│  - Query building                                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    MongoDB Database                          │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
backend/
├── repositories/           # NEW: Data access layer
│   ├── __init__.py
│   ├── base_repository.py  # Abstract base with common CRUD
│   └── ad_repository.py    # Ad-specific data operations
├── controllers/            # Business logic layer
│   └── gallery_controller.py  # Updated to use repository
├── models/                 # Data models and database connection
│   └── database.py
├── routes/                 # API routes
│   └── api_routes.py
└── services/               # External services (AI, storage, etc.)
```

## Components

### 1. Base Repository (`base_repository.py`)

Abstract base class providing common CRUD operations:

**Methods:**
- `find_by_id(doc_id)` - Find document by ID
- `find_one(query)` - Find single document
- `find_many(query, skip, limit, sort)` - Find multiple documents
- `count(query)` - Count documents
- `insert_one(document)` - Insert document
- `update_one(query, update)` - Update document
- `update_by_id(doc_id, update)` - Update by ID
- `delete_one(query)` - Delete document
- `delete_by_id(doc_id)` - Delete by ID
- `delete_many(query)` - Delete multiple documents
- `aggregate(pipeline)` - Run aggregation
- `distinct(field, query)` - Get distinct values

### 2. Ad Repository (`ad_repository.py`)

Specialized repository for ad/image operations:

**Methods:**
- `create_ad(workspace_id, prompt, params, images, size, mode)` - Create new ad
- `get_ad_by_id(ad_id)` - Get ad by ID
- `get_ads_by_workspace(workspace_id, skip, limit, aspect_ratio)` - Get ads with pagination
- `update_ad_metadata(ad_id, params, custom_note, tags)` - Update ad metadata
- `remove_image_from_ad(ad_id, filename)` - Remove specific image
- `delete_ad(ad_id)` - Delete ad
- `delete_ads_by_workspace(workspace_id)` - Delete all workspace ads
- `get_workspace_stats(workspace_id)` - Get workspace statistics
- `get_all_workspaces()` - List all workspaces
- `get_global_stats()` - Get global statistics
- `get_workspace_counts()` - Get ad count per workspace

### 3. Gallery Controller (`gallery_controller.py`)

Updated to use repository pattern:

**Changes:**
- Removed direct MongoDB operations
- Uses `ad_repository` for all data access
- Cleaner, more focused business logic
- Better error handling
- Easier to test

## Benefits

### 1. Separation of Concerns
- **Controllers**: Handle HTTP requests/responses and business logic
- **Repositories**: Handle data access and queries
- **Models**: Define data structure

### 2. Testability
- Easy to mock repositories for unit testing
- Can test business logic without database
- Can test data access logic independently

### 3. Maintainability
- Changes to data access don't affect business logic
- Easier to understand and modify
- Consistent patterns across codebase

### 4. Reusability
- Repository methods can be used by multiple controllers
- Common operations defined once in base repository
- Easy to add new repositories for other entities

### 5. Flexibility
- Easy to switch databases (just implement new repository)
- Can add caching layer in repository
- Can add query optimization without changing controllers

## Usage Examples

### Creating an Ad

```python
# In controller
ad_id = ad_repository.create_ad(
    workspace_id="default",
    prompt="Professional business ad",
    params={"category": "Business"},
    images=[{"filename": "img.png", "url": "https://..."}],
    size="1024x1024"
)
```

### Getting Ads with Pagination

```python
# In controller
ads, total = ad_repository.get_ads_by_workspace(
    workspace_id="default",
    skip=0,
    limit=50,
    aspect_ratio="instagram_post"
)
```

### Updating Ad Metadata

```python
# In controller
success = ad_repository.update_ad_metadata(
    ad_id="123abc",
    params={"updated": True},
    tags=["featured", "promoted"]
)
```

### Getting Statistics

```python
# In controller
stats = ad_repository.get_workspace_stats("default")
# Returns: {"total_ads": 100, "total_images": 300, "workspace_id": "default"}
```

## Migration Guide

### Before (Direct MongoDB Access)

```python
def get_all_ads():
    ads_collection = db.get_collection()
    ads = list(ads_collection.find({"workspace_id": workspace_id}))
    return jsonify({"ads": ads})
```

### After (Repository Pattern)

```python
def get_all_ads():
    ads, total = ad_repository.get_ads_by_workspace(workspace_id)
    return jsonify({"ads": ads, "total": total})
```

## Adding New Repositories

To add a new repository (e.g., for users):

1. **Create repository file**: `repositories/user_repository.py`

```python
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    def get_collection_name(self):
        return "users"
    
    def create_user(self, email, name):
        return self.insert_one({
            "email": email,
            "name": name,
            "created_at": datetime.now(timezone.utc)
        })
    
    def get_user_by_email(self, email):
        return self.find_one({"email": email})
```

2. **Update `__init__.py`**:

```python
from .ad_repository import AdRepository
from .user_repository import UserRepository

__all__ = ['AdRepository', 'UserRepository']
```

3. **Initialize in controller**:

```python
user_repository = UserRepository(db.get_collection("users"))
```

## Testing

### Unit Testing Controllers

```python
def test_save_to_gallery():
    # Mock repository
    mock_repo = Mock(spec=AdRepository)
    mock_repo.create_ad.return_value = "123abc"
    
    # Test controller logic
    result = save_to_gallery()
    
    # Verify repository was called correctly
    mock_repo.create_ad.assert_called_once()
```

### Integration Testing Repositories

```python
def test_ad_repository():
    # Use test database
    test_collection = test_db.get_collection("test_ads")
    repo = AdRepository(test_collection)
    
    # Test create
    ad_id = repo.create_ad(...)
    assert ad_id is not None
    
    # Test retrieve
    ad = repo.get_ad_by_id(ad_id)
    assert ad["workspace_id"] == "test"
```

## Best Practices

1. **Keep repositories focused** - One repository per entity/collection
2. **Use type hints** - Helps with IDE autocomplete and documentation
3. **Handle errors gracefully** - Return None or empty lists on errors
4. **Log operations** - Use print statements for debugging
5. **Document methods** - Clear docstrings for all public methods
6. **Avoid business logic** - Repositories should only handle data access
7. **Return consistent types** - Always return same type (e.g., list, not None)

## Performance Considerations

### Indexing

Repositories can create indexes for better performance:

```python
def create_indexes(self):
    self.collection.create_index([
        ("workspace_id", 1),
        ("created_at", -1)
    ])
```

### Caching

Add caching layer in repository:

```python
def get_ad_by_id(self, ad_id):
    # Check cache first
    cached = cache.get(f"ad:{ad_id}")
    if cached:
        return cached
    
    # Query database
    ad = self.find_by_id(ad_id)
    
    # Cache result
    if ad:
        cache.set(f"ad:{ad_id}", ad, ttl=300)
    
    return ad
```

## Troubleshooting

### Repository Not Initialized

**Error**: `Repository not initialized`

**Solution**: Ensure `init_repository()` is called in `app.py` after database connection

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'repositories'`

**Solution**: Ensure `repositories/__init__.py` exists and imports are correct

### Type Errors

**Error**: `'NoneType' object has no attribute 'find_one'`

**Solution**: Check that collection is passed to repository constructor

## Future Enhancements

1. **Add more repositories** - User, Workspace, Template repositories
2. **Implement caching** - Redis or in-memory caching
3. **Add query builders** - Fluent interface for complex queries
4. **Implement soft deletes** - Mark as deleted instead of removing
5. **Add audit logging** - Track all data changes
6. **Implement pagination helpers** - Standardized pagination across all repositories

---

**Status**: ✅ Implemented  
**Last Updated**: December 10, 2025  
**Version**: 1.0
