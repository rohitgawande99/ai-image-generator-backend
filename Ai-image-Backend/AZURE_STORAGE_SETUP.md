# Azure Blob Storage Setup Guide

This application uses Azure Blob Storage to store generated images in the cloud instead of local disk storage.

## Benefits

- **Scalability**: Store unlimited images without worrying about local disk space
- **Reliability**: Azure provides 99.9% uptime SLA
- **Performance**: Fast CDN-backed image delivery
- **Cost-effective**: Pay only for what you use
- **Accessibility**: Images accessible from anywhere via URL

## Prerequisites

1. Azure account (free tier available)
2. Azure Storage Account created
3. Blob container created

## Setup Steps

### 1. Create Azure Storage Account

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → "Storage account"
3. Fill in the details:
   - **Subscription**: Your Azure subscription
   - **Resource group**: Create new or use existing
   - **Storage account name**: Choose a unique name (e.g., `myappimages`)
   - **Region**: Choose closest to your users
   - **Performance**: Standard
   - **Redundancy**: LRS (Locally-redundant storage) for cost savings
4. Click "Review + create" → "Create"

### 2. Get Connection String

1. Go to your Storage Account
2. Click "Access keys" in the left menu
3. Copy the "Connection string" from key1 or key2

### 3. Create Blob Container

1. In your Storage Account, click "Containers" in the left menu
2. Click "+ Container"
3. Name it `generated-images` (or your preferred name)
4. Set "Public access level" to "Blob (anonymous read access for blobs only)"
5. Click "Create"

### 4. Configure Environment Variables

Add these to your `.env` file:

```env
# Azure Blob Storage Configuration
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
AZURE_STORAGE_ACCOUNT_KEY=your_storage_account_key
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your_account;AccountKey=your_key;EndpointSuffix=core.windows.net
AZURE_STORAGE_CONTAINER_NAME=generated-images
```

**Example:**
```env
AZURE_STORAGE_ACCOUNT_NAME=myappimages
AZURE_STORAGE_ACCOUNT_KEY=abc123def456...
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=myappimages;AccountKey=abc123def456...;EndpointSuffix=core.windows.net
AZURE_STORAGE_CONTAINER_NAME=generated-images
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `azure-storage-blob==12.19.0`

### 6. Restart Backend Server

```bash
python app.py
```

You should see:
```
✅ Connected to Azure Blob Storage container: generated-images
```

## How It Works

### Image Upload Flow

1. **Image Generation**: AI generates image (Gemini or Azure FLUX)
2. **Azure Upload**: Image is uploaded to Azure Blob Storage
3. **URL Storage**: Only the Azure Blob URL is stored in MongoDB
4. **Frontend Display**: Frontend loads images directly from Azure CDN

### Fallback Mechanism

If Azure Blob Storage is not configured or fails:
- Images are saved to local `generated_images/` folder
- Local URLs are stored in MongoDB
- Images are served via Flask `/images/<filename>` route

### Database Structure

MongoDB stores only the image metadata and URL:

```json
{
  "_id": "...",
  "workspace_id": "default",
  "prompt": "...",
  "images": [
    {
      "filename": "default_category_abc123.png",
      "url": "https://myappimages.blob.core.windows.net/generated-images/default_category_abc123.png",
      "type": "base64",
      "storage": "azure"
    }
  ],
  "created_at": "2025-12-10T..."
}
```

## Verification

### Check if Azure Storage is Working

1. Generate an image in the app
2. Check backend logs for:
   ```
   📤 Uploading to Azure Blob Storage...
   ✅ Uploaded to Azure Blob Storage: default_category_abc123.png
   ```
3. Verify in Azure Portal:
   - Go to Storage Account → Containers → generated-images
   - You should see the uploaded images

### Check Image URLs

Images should have URLs like:
```
https://your-storage-account.blob.core.windows.net/generated-images/default_category_abc123.png
```

## Troubleshooting

### Error: "Azure Blob Storage not configured"

**Solution**: Check that `AZURE_STORAGE_CONNECTION_STRING` is set in `.env`

### Error: "Container not found"

**Solution**: 
1. Verify container name matches `AZURE_STORAGE_CONTAINER_NAME`
2. Check container exists in Azure Portal
3. Ensure container has public blob access

### Error: "Authentication failed"

**Solution**:
1. Verify connection string is correct
2. Check storage account key hasn't been regenerated
3. Ensure no extra spaces in `.env` values

### Images not displaying in gallery

**Solution**:
1. Check browser console for CORS errors
2. Verify container has "Blob (anonymous read access)" enabled
3. Test image URL directly in browser

## Cost Estimation

Azure Blob Storage pricing (as of 2025):

- **Storage**: ~$0.018 per GB/month
- **Operations**: 
  - Write: $0.05 per 10,000 operations
  - Read: $0.004 per 10,000 operations
- **Data transfer**: First 100 GB free/month

**Example**: 
- 1,000 images × 500 KB = 500 MB
- Monthly cost: ~$0.01 storage + minimal operations = **< $0.10/month**

## Security Best Practices

1. **Never commit** `.env` file to version control
2. **Rotate keys** regularly in Azure Portal
3. **Use SAS tokens** for temporary access (optional advanced feature)
4. **Enable soft delete** in Azure Portal for accidental deletion protection
5. **Monitor usage** in Azure Portal to detect unusual activity

## Migration from Local Storage

If you have existing images in local storage:

1. Keep local images as backup
2. New images will automatically use Azure
3. Old images will continue to work via local URLs
4. Optional: Manually migrate old images using Azure Storage Explorer

## Additional Resources

- [Azure Blob Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/)
- [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/) - GUI tool for managing blobs
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
