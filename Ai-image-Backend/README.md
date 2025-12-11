# AI Image Generation Backend

Professional AI-powered advertising image generator with dual model support, Azure Blob Storage, and clean MVC architecture.

## 🚀 Features

### Image Generation
- 🤖 **Dual AI Models**
  - Azure FLUX (Free) - Fast, reliable generation
  - Gemini 2.5 Flash Image (Premium) - High-quality results
- 🎨 **Smart Prompts** - Claude AI-enhanced prompt generation
- 📐 **Multiple Formats** - Square (1:1) optimized for all platforms
- 🖼️ **Full-Bleed** - Edge-to-edge professional compositions

### Storage & Data
- ☁️ **Azure Blob Storage** - Cloud storage with 10-year SAS URLs
- 💾 **MongoDB** - Flexible document storage
- 🔄 **Repository Pattern** - Clean data access layer
- 📊 **Mixed Schema** - Backward compatible with old documents

### Content Safety
- 🛡️ **Family-Friendly** - All content appropriate for all ages
- 👔 **Professional Attire** - Category-appropriate clothing
- ✅ **No 18+ Content** - Strict content safety guidelines

### Architecture
- 🏗️ **MVC Pattern** - Clean separation of concerns
- 📦 **Modular Design** - Easy to maintain and extend
- 🔌 **RESTful API** - Standard HTTP endpoints
- 🧪 **Testable** - Repository pattern enables easy testing

## 📋 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```env
# MongoDB (Required)
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
DB_NAME=image_generation-images
COLLECTION_NAME=images

# Azure FLUX (Free Model - Required)
AZURE_FLUX_API_KEY=your_azure_flux_api_key
AZURE_FLUX_ENDPOINT=your_azure_flux_endpoint

# Google Cloud Vertex AI (Premium Model - Optional)
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=service_account_key.json

# Claude AI (Prompt Enhancement - Required)
AZURE_CLAUDE_API_KEY=your_claude_api_key
AZURE_CLAUDE_ENDPOINT=your_claude_endpoint
CLAUDE_DEPLOYMENT_NAME=claude-opus-4-1

# Azure Blob Storage (Image Storage - Required)
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account
AZURE_STORAGE_ACCOUNT_KEY=your_storage_key
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_STORAGE_CONTAINER_NAME=generated-images

# Server
BASE_URL=http://localhost:5000
WORKSPACE_ID=default
```

### 3. Run Application

```bash
python app.py
```

Server starts at: **http://localhost:5000**

## 🏗️ Architecture

### Layered Structure

```
Routes → Controllers → Repositories → Database
                    ↓
                 Services (AI, Storage)
```

### Directory Structure

```
backend/
├── app.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
│
├── config/                     # Configuration
│   └── config.py              # Settings management
│
├── routes/                     # API routes
│   └── api_routes.py          # Endpoint definitions
│
├── controllers/                # Request handlers
│   ├── gallery_controller.py  # Gallery operations
│   ├── image_controller.py    # Image generation
│   ├── prompt_controller.py   # Prompt generation
│   ├── ai_controller.py       # AI analysis
│   └── config_controller.py   # Configuration
│
├── repositories/               # Data access layer
│   ├── base_repository.py     # Common CRUD operations
│   └── ad_repository.py       # Ad-specific operations
│
├── services/                   # Business logic
│   ├── image_service.py       # Image generation (Gemini/FLUX)
│   ├── prompt_service.py      # Prompt generation (Claude)
│   ├── ai_service.py          # AI analysis (Claude)
│   └── azure_storage_service.py # Cloud storage
│
├── models/                     # Data models
│   ├── database.py            # MongoDB connection
│   └── schema.py              # Document schemas
│
├── utils/                      # Utilities
│   ├── image_utils.py         # Image processing
│   └── serializers.py         # Data serialization
│
└── generated_images/           # Local fallback storage
```

## 🔌 API Endpoints

### Image Generation

**Generate Prompts**
```http
POST /api/generate-prompts
Content-Type: application/json

{
  "num_variations": 3,
  "params": {
    "product_name": "AI Workshop",
    "category": "Education",
    "headline": "Learn AI Today"
  }
}
```

**Generate Images**
```http
POST /api/generate-images
Content-Type: application/json

{
  "selected_prompt": "Professional advertising poster...",
  "params": {
    "image_model": "free",  // or "paid"
    "aspect_ratio": "instagram_post"
  },
  "num_images": 3
}
```

### Gallery Management

**Get All Ads**
```http
GET /api/ads?limit=50&skip=0&aspect_ratio=instagram_post
```

**Save to Gallery**
```http
POST /api/save-to-gallery
Content-Type: application/json

{
  "workspace_id": "default",
  "prompt": "...",
  "params": {...},
  "images": [...],
  "size": "1024x1024"
}
```

**Delete Ad**
```http
DELETE /api/ads/{ad_id}
```

### AI Features

**Auto-fill Fields**
```http
POST /api/autofill-fields
Content-Type: application/json

{
  "product_description": "AI Workshop for students",
  "category": "Education",
  "brand_name": "TechEdu"
}
```

**Analyze Image**
```http
POST /api/analyze-image
Content-Type: application/json

{
  "image": "base64_encoded_image_data"
}
```

### System

**Health Check**
```http
GET /api/health
```

**Get Configuration**
```http
GET /api/config
```

**Get Statistics**
```http
GET /api/stats
```

## 🎨 Image Generation Models

### Azure FLUX (Free)

**Best for**: Testing, prototypes, high volume  
**Cost**: Free  
**Speed**: ~30 seconds per image  
**Quality**: Good  
**Aspect Ratios**: All supported  

**Configuration**:
```env
AZURE_FLUX_API_KEY=your_key
AZURE_FLUX_ENDPOINT=your_endpoint
```

### Gemini 2.5 Flash Image (Premium)

**Best for**: Production, high-quality campaigns  
**Cost**: Paid (Google Cloud)  
**Speed**: ~20 seconds per image  
**Quality**: Premium  
**Aspect Ratios**: 1:1 (square) only  

**Configuration**:
```env
GOOGLE_CLOUD_PROJECT=your_project
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=key.json
```

### Model Selection

Users select model in frontend:
- Frontend sends: `image_model: "free"` or `"paid"`
- Backend routes to appropriate API
- Automatic fallback if model unavailable

## ☁️ Azure Blob Storage

### Setup

1. Create Azure Storage Account
2. Create container: `generated-images`
3. Get connection string from Access Keys
4. Configure in `.env`

### Features

- **Cloud Storage**: Unlimited capacity
- **SAS URLs**: 10-year validity
- **Private Container**: Secure access
- **Automatic Fallback**: Uses local storage if Azure fails
- **CDN Delivery**: Fast global access

### URL Format

```
https://account.blob.core.windows.net/container/file.png?sv=2023-11-03&st=...&se=...&sr=b&sp=r&sig=...
```

## 💾 MongoDB Schema

### Ad Document

```json
{
  "_id": "ObjectId",
  "workspace_id": "default",
  "prompt": "Full generation prompt...",
  "params": {
    "category": "Education",
    "product_name": "AI Workshop",
    "headline": "Learn AI Today",
    "image_model": "free",
    "num_variations": 3,
    "aspect_ratio": "instagram_post"
  },
  "images": [
    {
      "filename": "default_Education_abc123.png",
      "url": "https://account.blob.core.windows.net/...",
      "type": "base64",
      "storage": "azure"
    }
  ],
  "mode": "custom",
  "size": "1024x1024",
  "created_at": "2025-12-10T10:30:00.000Z",
  "updated_at": "2025-12-10T10:30:00.000Z"
}
```

## 🛡️ Content Safety

### Guidelines

- ✅ Family-friendly content only
- ✅ Professional, modest attire
- ✅ Category-appropriate clothing
- ✅ Appropriate for all ages
- ❌ No revealing clothing
- ❌ No suggestive poses
- ❌ No 18+ content

### Implementation

- Base prompts include safety instructions
- Claude AI receives explicit guidelines
- AI models have built-in content filters
- Category-appropriate attire specified

### Model Distribution

- Variation 1: Professional Man (Right)
- Variation 2: Professional Man (Left)
- Variation 3: Professional Woman (Left)

## 📚 Documentation

### Setup & Configuration
- `AZURE_STORAGE_SETUP.md` - Azure Blob Storage setup
- `AZURE_STORAGE_QUICK_START.md` - Quick 5-minute setup
- `.env.example` - Configuration template

### Architecture & Design
- `ARCHITECTURE.md` - Complete architecture overview
- `REPOSITORY_PATTERN.md` - Repository pattern details
- `MODEL_SWITCHING_FLOW.md` - Model selection flow

### Features & Updates
- `FULL_BLEED_IMAGES.md` - Image composition guidelines
- `CONTENT_SAFETY_GUIDELINES.md` - Content safety rules
- `PROMPT_VARIATIONS_UPDATE.md` - Prompt variation details

### Database & Migration
- `MONGODB_SCHEMA_UPDATE.md` - Schema changes
- `MONGODB_MIGRATION_GUIDE.md` - Migration guide
- `add_missing_fields.py` - Migration script

### Storage & Cleanup
- `LOCAL_STORAGE_INFO.md` - Local storage info
- `cleanup_local_images.py` - Cleanup script

## 🔧 Troubleshooting

### Azure Blob Storage Issues

**Error**: "Azure Blob Storage not configured"  
**Solution**: Check `AZURE_STORAGE_CONNECTION_STRING` in `.env`

**Error**: "Container not found"  
**Solution**: Create container in Azure Portal or let app create it

**Error**: "Public access not permitted"  
**Solution**: App uses private container with SAS tokens (this is correct)

### MongoDB Issues

**Error**: "Database not connected"  
**Solution**: Check `MONGO_URI` in `.env`, ensure MongoDB is accessible

**Error**: "Collection not found"  
**Solution**: Collection is created automatically on first use

### Image Generation Issues

**Error**: "Image service not initialized"  
**Solution**: Check API keys in `.env`, restart application

**Error**: "Model not available"  
**Solution**: Verify credentials for selected model (Azure FLUX or Gemini)

### General Issues

**Error**: "Module not found"  
**Solution**: Run `pip install -r requirements.txt`

**Error**: "Port already in use"  
**Solution**: Change port in `config.py` or stop other process

## 🧪 Testing

### Test Azure Storage

```bash
python quick_azure_test.py
```

### Test Image Generation

```bash
python test_vertex_ai.py
```

### Verify Setup

```bash
python verify_setup.py
```

## 📦 Dependencies

### Core
- Flask 3.0.0 - Web framework
- pymongo 4.6.1 - MongoDB driver
- python-dotenv 1.0.0 - Environment management

### AI & ML
- google-genai - Gemini API
- anthropic 0.40.0 - Claude AI
- Pillow 10.1.0 - Image processing

### Cloud Services
- azure-storage-blob 12.19.0 - Azure Blob Storage
- requests 2.32.3 - HTTP client

## 🚀 Deployment

### Environment Variables

Ensure all required variables are set:
- MongoDB connection
- Azure FLUX credentials
- Claude AI credentials
- Azure Blob Storage credentials
- (Optional) Google Cloud credentials

### Production Checklist

- [ ] Configure production MongoDB
- [ ] Set up Azure Blob Storage
- [ ] Configure API keys
- [ ] Set `DEBUG=False` in config
- [ ] Use production `BASE_URL`
- [ ] Set up monitoring
- [ ] Configure backups

## 📄 License

MIT

## 🤝 Support

For issues and questions:
1. Check documentation in `/backend/*.md` files
2. Review troubleshooting section
3. Check logs for error details

---

**Last Updated**: December 10, 2025  
**Version**: 2.0 (MVC + Azure + Repository Pattern)
