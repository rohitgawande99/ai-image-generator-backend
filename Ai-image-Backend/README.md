# Social Media Ad Generator

AI-powered social media ad generator using Google Vertex AI Gemini 2.5 Flash Image and Claude AI.

## 🎉 NEW: MVC Architecture (v2.0)

This backend has been **refactored into a clean MVC architecture** for better maintainability!

### 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes ⚡
- **[MVC_STRUCTURE.md](MVC_STRUCTURE.md)** - Architecture details 🏗️
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Visual diagrams 📊
- **[COMPARISON_GUIDE.md](COMPARISON_GUIDE.md)** - Before/After 🔍
- **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)** - Migration info 📈

### ✨ What Changed

- **97% smaller** main file (1,798 → 56 lines)
- **15 focused modules** instead of 1 huge file
- **Better organized** - MVC pattern
- **Easier to maintain** and extend
- **All functionality preserved** ✅

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and configure:
```env
# Google Cloud Vertex AI (Required for Image Generation)
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path_to_service_account.json

# AI Enhancement (Required)
AZURE_CLAUDE_API_KEY=your_claude_api_key
AZURE_CLAUDE_ENDPOINT=your_claude_endpoint

# Database (Required)
MONGO_URI=mongodb://localhost:27017/
DB_NAME=ad_generator_db
COLLECTION_NAME=generated_ads

# Server
BASE_URL=http://localhost:5000
WORKSPACE_ID=default
```

### 3. Start MongoDB
```bash
mongod
```

Or use MongoDB Atlas (cloud) and update `MONGO_URI` in `.env`.

### 4. Run the Application
```bash
python app.py
```

### 5. Open Browser
Navigate to: **http://localhost:5000**

## Features

- 🎨 **Gemini 2.5 Flash Image** - Google's latest image generation model via Vertex AI
- 🤖 **Claude AI** - Intelligent prompt enhancement
- 📱 **Multiple Formats** - Instagram, Facebook, YouTube, etc.
- 💾 **Gallery** - Save and manage your favorite ads
- 🖼️ **Image Upload** - Analyze existing ads and recreate them
- 📤 **Easy Export** - Download images individually

## Usage Flow

1. **Fill Form** - Enter product details, text, pricing, etc.
2. **Auto-Fill (Optional)** - Let AI fill fields for you
3. **Upload Image (Optional)** - Analyze existing ad to extract details
4. **Generate Prompts** - AI creates 3 variations
5. **Select Prompt** - Choose your favorite
6. **Generate Images** - Create 1-3 images
7. **Save to Gallery** - Click individual save buttons on images you like
8. **View Gallery** - Browse and manage saved ads

## API Endpoints

### Generation
- `POST /api/generate-prompts` - Generate prompt variations
- `POST /api/generate-images` - Generate images with Gemini 2.5 Flash Image
- `POST /api/autofill-fields` - AI auto-fill form fields
- `POST /api/analyze-image` - Analyze uploaded image

### Gallery
- `GET /api/ads` - Get all saved ads
- `POST /api/save-to-gallery` - Save specific images
- `DELETE /api/delete-all-ads` - Delete all ads
- `DELETE /api/ads/:id` - Delete specific ad

### Other
- `GET /api/config` - Get configuration options
- `GET /api/stats` - Get gallery statistics
- `GET /api/health` - Health check

## Project Structure

```
flask api - Copy/
├── app.py                  # Main Flask application
├── prompt_expander.py      # Claude AI prompt enhancement
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── templates/              # HTML templates
│   ├── index.html         # Main generator page
│   └── gallery.html       # Gallery page
├── static/                 # Frontend assets
│   └── app.js             # JavaScript logic
└── generated_images/       # Saved images
```

## Troubleshooting

### "No module named 'vertexai'"
```bash
pip install google-cloud-aiplatform
```

### "MongoDB connection error"
- Ensure MongoDB is running: `mongod`
- Or update `MONGO_URI` in `.env` with cloud connection string

### "Image generation model not initialized"
- Check `GOOGLE_APPLICATION_CREDENTIALS` path in `.env`
- Verify service account JSON file exists
- Ensure Vertex AI API is enabled in Google Cloud Console
- Verify service account has 'Vertex AI User' role
- Restart the application

### "Permission denied" or "Credentials error"
- Verify `GOOGLE_CLOUD_PROJECT` matches your GCP project ID
- Check service account has proper permissions
- Ensure Vertex AI API is enabled in your project

### "Claude API error"
- Check `AZURE_CLAUDE_API_KEY` and `AZURE_CLAUDE_ENDPOINT` in `.env`
- Verify credentials are correct

## Requirements

- Python 3.8+
- MongoDB (local or cloud)
- Google Cloud Project with Vertex AI API enabled
- Google Cloud Service Account with Vertex AI User role
- Claude API key
- Internet connection

## Key Technologies

- **Backend**: Flask, Python
- **Image Generation**: Gemini 2.5 Flash Image via Google Vertex AI
- **AI Enhancement**: Claude AI (Anthropic)
- **Database**: MongoDB
- **Frontend**: Vanilla JavaScript, HTML, CSS

## License

MIT
