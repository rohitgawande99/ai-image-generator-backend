# Backend Architecture

## Overview

The backend follows a **layered architecture** with clear separation of concerns using the **Repository Pattern**.

## Layers

### 1. Routes Layer (`routes/`)
- **Purpose**: Define API endpoints
- **Responsibilities**: URL routing, HTTP method mapping
- **Files**: `api_routes.py`

### 2. Controllers Layer (`controllers/`)
- **Purpose**: Handle HTTP requests and responses
- **Responsibilities**:
  - Request validation
  - Response formatting
  - Business logic orchestration
  - Error handling
- **Files**:
  - `gallery_controller.py` - Ad/image gallery operations
  - `image_controller.py` - Image generation
  - `prompt_controller.py` - Prompt generation
  - `ai_controller.py` - AI analysis and autofill
  - `config_controller.py` - Configuration endpoints

### 3. Repositories Layer (`repositories/`) ✨ NEW
- **Purpose**: Data access abstraction
- **Responsibilities**:
  - MongoDB operations
  - Query building
  - Data persistence
  - CRUD operations
- **Files**:
  - `base_repository.py` - Abstract base with common operations
  - `ad_repository.py` - Ad-specific data operations

### 4. Services Layer (`services/`)
- **Purpose**: External integrations and complex business logic
- **Responsibilities**:
  - AI model interactions
  - Cloud storage operations
  - Third-party API calls
- **Files**:
  - `image_service.py` - Image generation (Gemini/Azure FLUX)
  - `prompt_service.py` - Prompt generation (Claude AI)
  - `ai_service.py` - AI analysis (Claude)
  - `azure_storage_service.py` - Azure Blob Storage
  - `user_service.py` - User management

### 5. Models Layer (`models/`)
- **Purpose**: Data models and database connection
- **Responsibilities**:
  - Database connection management
  - Schema definitions
  - Data validation
- **Files**:
  - `database.py` - MongoDB connection
  - `schema.py` - Document schemas

### 6. Utils Layer (`utils/`)
- **Purpose**: Helper functions and utilities
- **Responsibilities**:
  - Image processing
  - Data serialization
  - Common utilities
- **Files**:
  - `image_utils.py` - Image operations
  - `serializers.py` - Data serialization

### 7. Config Layer (`config/`)
- **Purpose**: Application configuration
- **Responsibilities**:
  - Environment variables
  - Application settings
  - Constants
- **Files**:
  - `config.py` - Configuration management

## Request Flow

```
1. Client Request
   ↓
2. Routes (api_routes.py)
   - Maps URL to controller function
   ↓
3. Controller (e.g., gallery_controller.py)
   - Validates request
   - Calls repository for data
   - Calls services for business logic
   ↓
4. Repository (e.g., ad_repository.py)
   - Executes MongoDB queries
   - Returns data
   ↓
5. Service (e.g., image_service.py)
   - Performs complex operations
   - Interacts with external APIs
   ↓
6. Controller
   - Formats response
   - Returns JSON
   ↓
7. Client Response
```

## Example: Saving an Image to Gallery

```python
# 1. Route (api_routes.py)
api_bp.route('/save-to-gallery', methods=['POST'])(gallery_controller.save_to_gallery)

# 2. Controller (gallery_controller.py)
def save_to_gallery():
    data = request.get_json()
    
    # 3. Repository call
    ad_id = ad_repository.create_ad(
        workspace_id=data["workspace_id"],
        prompt=data["prompt"],
        params=data["params"],
        images=data["images"],
        size=data["size"]
    )
    
    return jsonify({"success": True, "ad_id": ad_id})

# 4. Repository (ad_repository.py)
def create_ad(self, workspace_id, prompt, params, images, size):
    document = {
        "workspace_id": workspace_id,
        "prompt": prompt,
        "params": params,
        "images": images,
        "size": size,
        "created_at": datetime.now(timezone.utc)
    }
    return self.insert_one(document)

# 5. Base Repository (base_repository.py)
def insert_one(self, document):
    result = self.collection.insert_one(document)
    return str(result.inserted_id)
```

## Design Principles

### 1. Single Responsibility
Each layer has one clear purpose:
- Routes: Routing
- Controllers: Request/response handling
- Repositories: Data access
- Services: Business logic
- Models: Data structure

### 2. Dependency Inversion
- Controllers depend on repository interfaces, not implementations
- Easy to swap implementations (e.g., different databases)

### 3. Don't Repeat Yourself (DRY)
- Common CRUD operations in base repository
- Reusable utilities in utils layer
- Shared configuration in config layer

### 4. Separation of Concerns
- Data access logic separate from business logic
- External integrations isolated in services
- Clear boundaries between layers

## Benefits

### ✅ Maintainability
- Easy to locate and fix bugs
- Clear structure for new developers
- Consistent patterns throughout

### ✅ Testability
- Each layer can be tested independently
- Easy to mock dependencies
- Unit tests for business logic
- Integration tests for data access

### ✅ Scalability
- Easy to add new features
- Can optimize individual layers
- Can scale services independently

### ✅ Flexibility
- Easy to swap implementations
- Can add caching, logging, etc.
- Can change databases without affecting business logic

## File Organization

```
backend/
├── app.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
│
├── config/                 # Configuration
│   ├── __init__.py
│   └── config.py
│
├── routes/                 # API routes
│   ├── __init__.py
│   └── api_routes.py
│
├── controllers/            # Request handlers
│   ├── __init__.py
│   ├── gallery_controller.py
│   ├── image_controller.py
│   ├── prompt_controller.py
│   ├── ai_controller.py
│   └── config_controller.py
│
├── repositories/           # Data access ✨ NEW
│   ├── __init__.py
│   ├── base_repository.py
│   └── ad_repository.py
│
├── services/               # Business logic & external APIs
│   ├── __init__.py
│   ├── image_service.py
│   ├── prompt_service.py
│   ├── ai_service.py
│   ├── azure_storage_service.py
│   └── user_service.py
│
├── models/                 # Data models
│   ├── __init__.py
│   ├── database.py
│   └── schema.py
│
├── utils/                  # Utilities
│   ├── __init__.py
│   ├── image_utils.py
│   └── serializers.py
│
└── generated_images/       # Local image storage (fallback)
```

## Technology Stack

- **Framework**: Flask 3.0.0
- **Database**: MongoDB (via pymongo)
- **AI Models**:
  - Google Gemini 2.5 Flash Image (paid)
  - Azure FLUX (free)
  - Claude Opus 4.1 (prompt generation)
- **Storage**: Azure Blob Storage
- **Image Processing**: Pillow
- **HTTP Client**: requests

## Environment Variables

See `.env.example` for all configuration options:
- MongoDB connection
- Google Cloud credentials
- Azure API keys
- Storage configuration
- Workspace settings

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run application**:
   ```bash
   python app.py
   ```

4. **Access API**:
   - Base URL: `http://localhost:5000`
   - API endpoints: `http://localhost:5000/api/*`

## API Documentation

See individual controller files for endpoint documentation:
- Gallery: `controllers/gallery_controller.py`
- Images: `controllers/image_controller.py`
- Prompts: `controllers/prompt_controller.py`
- AI: `controllers/ai_controller.py`

## Further Reading

- [Repository Pattern](REPOSITORY_PATTERN.md) - Detailed repository documentation
- [Azure Storage Setup](AZURE_STORAGE_SETUP.md) - Cloud storage configuration
- [Full-Bleed Images](FULL_BLEED_IMAGES.md) - Image generation guidelines
- [Model Switching](MODEL_SWITCHING_GUIDE.md) - AI model configuration

---

**Last Updated**: December 10, 2025  
**Architecture Version**: 2.0 (with Repository Pattern)
