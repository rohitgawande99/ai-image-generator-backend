"""
Image processing utilities
"""
import os
import base64
import uuid
import requests
from config.config import Config


def sanitize_filename(text):
    """Sanitize text for use in filename"""
    # Replace spaces and special characters with underscores
    import re
    sanitized = re.sub(r'[^\w\-]', '_', text)
    # Remove consecutive underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized.strip('_')


def save_base64_image(base64_data, workspace_id, category="general"):
    """
    Save base64 image to Azure Blob Storage (preferred) or local disk (fallback)
    
    Returns URL from Azure Blob Storage if available, otherwise local URL
    """
    try:
        # Try Azure Blob Storage first
        from services.azure_storage_service import azure_storage_service
        
        if azure_storage_service.is_available():
            print(f"  📤 Uploading to Azure Blob Storage...")
            result = azure_storage_service.upload_base64_image(base64_data, workspace_id, category)
            if result["success"]:
                return result
            else:
                print(f"  ⚠️  Azure upload failed, falling back to local storage")
        
        # Fallback to local storage
        print(f"  💾 Saving to local storage...")
        safe_category = sanitize_filename(category)
        filename = f"{workspace_id}_{safe_category}_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        image_data = base64.b64decode(base64_data)
        with open(filepath, "wb") as f:
            f.write(image_data)
        
        image_url = f"{Config.BASE_URL}/images/{filename}"
        
        return {
            "success": True,
            "filename": filename,
            "filepath": filepath,
            "url": image_url,
            "storage": "local"
        }
    except Exception as e:
        print(f"  ❌ Error saving image: {e}")
        return {"success": False, "error": str(e)}


def download_image_from_url(image_url, workspace_id, category="general"):
    """
    Download image from URL and save to Azure Blob Storage (preferred) or local disk (fallback)
    """
    try:
        # Try Azure Blob Storage first
        from services.azure_storage_service import azure_storage_service
        
        if azure_storage_service.is_available():
            print(f"  📤 Uploading to Azure Blob Storage...")
            result = azure_storage_service.upload_image_from_url(image_url, workspace_id, category)
            if result["success"]:
                return result
            else:
                print(f"  ⚠️  Azure upload failed, falling back to local storage")
        
        # Fallback to local storage
        print(f"  💾 Saving to local storage...")
        response = requests.get(image_url)
        response.raise_for_status()
        
        safe_category = sanitize_filename(category)
        filename = f"{workspace_id}_{safe_category}_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        local_url = f"{Config.BASE_URL}/images/{filename}"
        
        return {
            "success": True,
            "filename": filename,
            "filepath": filepath,
            "url": local_url,
            "storage": "local"
        }
    except Exception as e:
        print(f"  ❌ Error downloading image: {e}")
        return {"success": False, "error": str(e)}


def delete_image_file(filename):
    """Delete image file from Azure Blob Storage or local disk"""
    try:
        # Try deleting from Azure Blob Storage first
        from services.azure_storage_service import azure_storage_service
        
        if azure_storage_service.is_available():
            if azure_storage_service.blob_exists(filename):
                return azure_storage_service.delete_blob(filename)
        
        # Fallback to local storage
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"  ⚠️  Error deleting image: {e}")
        return False


def convert_image_to_png(base64_data):
    """Convert any image format to PNG using PIL"""
    try:
        from PIL import Image
        import io
        
        print(f"  🔄 Converting image to PNG...")
        
        image_bytes = base64.b64decode(base64_data)
        img = Image.open(io.BytesIO(image_bytes))
        
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        output = io.BytesIO()
        img.save(output, format='PNG', optimize=True)
        output.seek(0)
        
        png_base64 = base64.b64encode(output.read()).decode('utf-8')
        
        print(f"  ✅ Converted to PNG ({len(png_base64)} chars)")
        
        return png_base64, "image/png"
        
    except Exception as e:
        print(f"  ❌ Conversion failed: {e}")
        return None, None


def detect_image_type(base64_data):
    """Detect image type from base64 data"""
    try:
        sample_size = min(200, len(base64_data))
        header = base64.b64decode(base64_data[:sample_size])
        
        if header.startswith(b'\xff\xd8\xff'):
            return "image/jpeg"
        elif header.startswith(b'\x89PNG\r\n\x1a\n'):
            return "image/png"
        elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return "image/gif"
        elif header.startswith(b'RIFF') and b'WEBP' in header[:20]:
            return "image/webp"
        elif header.startswith(b'BM'):
            return "image/bmp"
        elif header.startswith(b'II*\x00') or header.startswith(b'MM\x00*'):
            return "image/tiff"
        elif header.startswith(b'\x00\x00\x01\x00'):
            return "image/x-icon"
        elif header.startswith(b'<') or header.startswith(b'<?xml'):
            return "image/svg+xml"
        elif b'ftyp' in header[:20] and b'avif' in header[:20]:
            return "image/avif"
        elif b'ftyp' in header[:20] and (b'heic' in header[:20] or b'mif1' in header[:20]):
            return "image/heic"
        else:
            print(f"  ⚠️  Unknown image type, defaulting to image/png")
            return "image/png"
            
    except Exception as e:
        print(f"  ⚠️  Error detecting image type: {e}, defaulting to image/png")
        return "image/png"
