"""
Azure Blob Storage service for image storage
"""
import os
import uuid
import base64
import io
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, ContentSettings, generate_blob_sas, BlobSasPermissions
from config.config import Config


class AzureStorageService:
    """Service for Azure Blob Storage operations"""
    
    def __init__(self):
        self.connection_string = Config.AZURE_STORAGE_CONNECTION_STRING
        self.container_name = Config.AZURE_STORAGE_CONTAINER_NAME
        self.account_name = Config.AZURE_STORAGE_ACCOUNT_NAME
        self.account_key = Config.AZURE_STORAGE_ACCOUNT_KEY
        self.blob_service_client = None
        self.container_client = None
        
        if self.connection_string:
            try:
                self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                self.container_client = self.blob_service_client.get_container_client(self.container_name)
                
                # Create container if it doesn't exist (private container)
                if not self.container_client.exists():
                    # Create private container (no public access)
                    self.container_client.create_container()
                    print(f"✅ Created Azure Blob Storage container: {self.container_name} (private)")
                else:
                    print(f"✅ Connected to Azure Blob Storage container: {self.container_name}")
                    
            except Exception as e:
                print(f"⚠️  Azure Blob Storage initialization error: {e}")
                self.blob_service_client = None
                self.container_client = None
        else:
            print("⚠️  Azure Blob Storage not configured (missing connection string)")
    
    def is_available(self):
        """Check if Azure Blob Storage is available"""
        return self.container_client is not None
    
    def upload_base64_image(self, base64_data, workspace_id, category="general"):
        """
        Upload base64 image to Azure Blob Storage
        
        Args:
            base64_data: Base64 encoded image data
            workspace_id: Workspace identifier
            category: Image category
            
        Returns:
            dict: Upload result with success status, filename, and URL
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "Azure Blob Storage not configured"
            }
        
        try:
            # Sanitize category name
            safe_category = self._sanitize_filename(category)
            
            # Generate unique filename
            filename = f"{workspace_id}_{safe_category}_{uuid.uuid4().hex[:8]}.png"
            
            # Decode base64 data
            image_data = base64.b64decode(base64_data)
            
            # Upload to Azure Blob Storage
            blob_client = self.container_client.get_blob_client(filename)
            
            # Set content type for proper image display
            content_settings = ContentSettings(content_type='image/png')
            
            blob_client.upload_blob(
                image_data,
                overwrite=True,
                content_settings=content_settings
            )
            
            # Generate SAS URL for private blob (valid for 10 years)
            blob_url = self._generate_blob_url_with_sas(filename)
            
            print(f"  ✅ Uploaded to Azure Blob Storage: {filename}")
            
            return {
                "success": True,
                "filename": filename,
                "url": blob_url,
                "storage": "azure"
            }
            
        except Exception as e:
            print(f"  ❌ Azure Blob Storage upload error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def upload_image_from_url(self, image_url, workspace_id, category="general"):
        """
        Download image from URL and upload to Azure Blob Storage
        
        Args:
            image_url: URL of the image to download
            workspace_id: Workspace identifier
            category: Image category
            
        Returns:
            dict: Upload result with success status, filename, and URL
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "Azure Blob Storage not configured"
            }
        
        try:
            import requests
            
            # Download image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Sanitize category name
            safe_category = self._sanitize_filename(category)
            
            # Generate unique filename
            filename = f"{workspace_id}_{safe_category}_{uuid.uuid4().hex[:8]}.png"
            
            # Upload to Azure Blob Storage
            blob_client = self.container_client.get_blob_client(filename)
            
            # Set content type
            content_settings = ContentSettings(content_type='image/png')
            
            blob_client.upload_blob(
                response.content,
                overwrite=True,
                content_settings=content_settings
            )
            
            # Generate SAS URL for private blob (valid for 10 years)
            blob_url = self._generate_blob_url_with_sas(filename)
            
            print(f"  ✅ Uploaded to Azure Blob Storage: {filename}")
            
            return {
                "success": True,
                "filename": filename,
                "url": blob_url,
                "storage": "azure"
            }
            
        except Exception as e:
            print(f"  ❌ Azure Blob Storage upload error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_blob(self, filename):
        """
        Delete blob from Azure Blob Storage
        
        Args:
            filename: Name of the blob to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        if not self.is_available():
            return False
        
        try:
            blob_client = self.container_client.get_blob_client(filename)
            blob_client.delete_blob()
            print(f"  ✅ Deleted from Azure Blob Storage: {filename}")
            return True
        except Exception as e:
            print(f"  ⚠️  Error deleting blob: {e}")
            return False
    
    def blob_exists(self, filename):
        """
        Check if blob exists in Azure Blob Storage
        
        Args:
            filename: Name of the blob to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        if not self.is_available():
            return False
        
        try:
            blob_client = self.container_client.get_blob_client(filename)
            return blob_client.exists()
        except:
            return False
    
    def _sanitize_filename(self, text):
        """Sanitize text for use in filename"""
        import re
        sanitized = re.sub(r'[^\w\-]', '_', text)
        sanitized = re.sub(r'_+', '_', sanitized)
        return sanitized.strip('_')
    
    def _generate_blob_url_with_sas(self, filename, expiry_years=10):
        """
        Generate blob URL with SAS token for private containers
        
        Args:
            filename: Name of the blob
            expiry_years: Number of years until SAS token expires (default: 10)
            
        Returns:
            str: Full blob URL with SAS token
        """
        try:
            # Generate SAS token with read permissions
            from datetime import timezone as tz
            sas_token = generate_blob_sas(
                account_name=self.account_name,
                container_name=self.container_name,
                blob_name=filename,
                account_key=self.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.now(tz.utc) + timedelta(days=365 * expiry_years)
            )
            
            # Construct full URL with SAS token
            blob_url = f"https://{self.account_name}.blob.core.windows.net/{self.container_name}/{filename}?{sas_token}"
            
            return blob_url
            
        except Exception as e:
            print(f"  ⚠️  Error generating SAS URL: {e}")
            # Fallback to basic URL (won't work for private containers)
            return f"https://{self.account_name}.blob.core.windows.net/{self.container_name}/{filename}"


# Global Azure Storage service instance
azure_storage_service = AzureStorageService()
