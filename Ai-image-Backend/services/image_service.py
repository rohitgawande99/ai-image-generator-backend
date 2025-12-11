"""
Image generation service
"""
import time
import base64
import json
import requests
from config.config import Config
from utils.image_utils import save_base64_image, download_image_from_url


class ImageService:
    """Service for image generation operations"""
    
    def __init__(self, genai_client, model_name="publishers/google/models/gemini-2.5-flash-image"):
        self.genai_client = genai_client
        self.model_name = model_name
        
        # Azure FLUX configuration for free users
        self.azure_flux_api_key = Config.AZURE_FLUX_API_KEY
        self.azure_flux_endpoint = Config.AZURE_FLUX_ENDPOINT
    
    def get_aspect_ratio_size(self, aspect_ratio_key):
        """Get image size for aspect ratio
        
        Gemini 2.5 Flash Image: Only supports 1:1 (square) - 1024x1024
        Azure FLUX: Supports any custom size
        
        Note: For paid users (Gemini), non-square ratios will generate as 1024x1024
        """
        aspect_mapping = {
            # Square (1:1) - Supported by both models
            "instagram_post": "1024x1024",
            "facebook_post": "1024x1024",
            "linkedin_post": "1024x1024",
            
            # Portrait (9:16) - Only Azure FLUX supports this
            "instagram_story": "1024x1792",
            "pinterest": "1024x1792",
            
            # Landscape (16:9) - Only Azure FLUX supports this
            "twitter_post": "1792x1024",
            "youtube_thumbnail": "1792x1024",
            "wide_banner": "1792x1024"
        }
        return aspect_mapping.get(aspect_ratio_key, "1024x1024")
    
    def generate_images(self, selected_prompt, params, num_images=3, is_paid_user=False):
        """Generate images using Gemini 2.5 Flash Image (paid) or Azure FLUX (free)"""
        workspace_id = Config.WORKSPACE_ID
        aspect_ratio_key = params.get("aspect_ratio", "instagram_post")
        size = self.get_aspect_ratio_size(aspect_ratio_key)
        
        # Determine which model to use
        if is_paid_user:
            model_type = "Gemini 2.5 Flash Image (Paid)"
            if self.genai_client is None:
                raise Exception("Google GenAI client not initialized. Please check Google Cloud credentials in .env file.")
        else:
            model_type = "Azure FLUX (Free)"
            if not self.azure_flux_api_key or not self.azure_flux_endpoint:
                raise Exception("Azure FLUX not configured. Please check AZURE_FLUX_API_KEY and AZURE_FLUX_ENDPOINT in .env file.")
        
        # Simple clear log
        print(f"\n{'='*80}")
        if is_paid_user:
            print(f"🤖 USING: Gemini 2.5 Flash Image (PAID) ✨")
        else:
            print(f"🤖 USING: Azure FLUX (FREE) 💰")
        print(f"📊 Generating {num_images} images | Size: {size}")
        print(f"{'='*80}")
        
        generated_images = []
        
        # Parse size
        width, height = map(int, size.split('x'))
        
        for img_idx in range(num_images):
            try:
                print(f"\n{'='*80}")
                print(f"  🎨 GENERATING IMAGE {img_idx + 1}/{num_images}")
                print(f"{'='*80}")
                
                if img_idx == 0:
                    print(f"  📝 PROMPT: {selected_prompt}")
                
                if img_idx > 0:
                    print(f"  ⏱️  Waiting 2 seconds before next request...")
                    time.sleep(2)
                
                if is_paid_user:
                    print(f"  ⏳ Calling Gemini API with size {width}x{height}...")
                else:
                    print(f"  ⏳ Calling Azure FLUX API with size {width}x{height}...")
                
                # Call appropriate API based on user type
                try:
                    if is_paid_user:
                        # Generate image using Gemini 2.5 Flash Image
                        # Note: Gemini 2.5 Flash Image currently only supports 1:1 (square) aspect ratio
                        # Non-square ratios will be generated as square and may need cropping
                        
                        if width != height:
                            print(f"  ⚠️  Note: Gemini 2.5 Flash Image only supports 1:1 (square) images")
                            print(f"  ⚠️  Requested {width}x{height} will be generated as 1024x1024")
                            print(f"  💡 Consider using Azure FLUX (free tier) for custom aspect ratios")
                        
                        # Call API (always generates 1024x1024)
                        response = self.genai_client.models.generate_content(
                            model=self.model_name,
                            contents=selected_prompt
                        )
                        
                        print(f"  ✅ API call completed")
                        
                        # Check if response has candidates with image data
                        if not hasattr(response, 'candidates') or not response.candidates:
                            print(f"  ⚠️  No candidates in response from Gemini")
                            continue
                        
                        # Extract image data from response
                        image_data = None
                        for candidate in response.candidates:
                            if hasattr(candidate, 'content') and candidate.content.parts:
                                for part in candidate.content.parts:
                                    if hasattr(part, 'inline_data') and part.inline_data:
                                        image_data = part.inline_data.data
                                        break
                            if image_data:
                                break
                        
                        if not image_data:
                            print(f"  ⚠️  No inline image data found in response")
                            continue
                        
                        # Convert bytes to base64
                        if isinstance(image_data, bytes):
                            image_base64 = base64.b64encode(image_data).decode('utf-8')
                        else:
                            image_base64 = image_data
                        
                        print(f"  🔍 Image received, size: {len(image_base64)} characters")
                    
                    else:
                        # Generate image using Azure FLUX (free users)
                        headers = {
                            "Content-Type": "application/json",
                            "api-key": self.azure_flux_api_key
                        }
                        
                        payload = {
                            "prompt": selected_prompt,
                            "n": 1,
                            "size": f"{width}x{height}"
                        }
                        
                        response = requests.post(
                            self.azure_flux_endpoint,
                            headers=headers,
                            json=payload,
                            timeout=60
                        )
                        
                        print(f"  ✅ API call completed")
                        
                        if response.status_code != 200:
                            print(f"  ❌ Azure FLUX API error: {response.status_code}")
                            print(f"  Response: {response.text}")
                            continue
                        
                        result = response.json()
                        
                        # Extract image from Azure FLUX response
                        if 'data' not in result or not result['data']:
                            print(f"  ⚠️  No image data in Azure FLUX response")
                            continue
                        
                        # Azure FLUX returns base64 or URL
                        image_item = result['data'][0]
                        if 'b64_json' in image_item:
                            image_base64 = image_item['b64_json']
                        elif 'url' in image_item:
                            # Download from URL
                            download_result = download_image_from_url(
                                image_item['url'],
                                workspace_id,
                                params.get("category", "general")
                            )
                            if download_result["success"]:
                                generated_images.append({
                                    "filename": download_result["filename"],
                                    "url": download_result["url"],
                                    "type": "url"
                                })
                                print(f"  ✅ Saved: {download_result['filename']}")
                            continue
                        else:
                            print(f"  ⚠️  Unknown Azure FLUX response format")
                            continue
                        
                        print(f"  🔍 Image received, size: {len(image_base64)} characters")
                    
                    # Save the image
                    save_result = save_base64_image(
                        image_base64,
                        workspace_id,
                        params.get("category", "general")
                    )
                    
                    if save_result["success"]:
                        generated_images.append({
                            "filename": save_result["filename"],
                            "url": save_result["url"],
                            "type": "base64"
                        })
                        print(f"  ✅ Saved: {save_result['filename']}")
                    
                except Exception as api_error:
                    error_msg = str(api_error)
                    print(f"  ❌ Vertex AI API call failed: {error_msg}")
                    print(f"  🔍 Error type: {type(api_error).__name__}")
                    
                    # Provide helpful error messages
                    if "permission" in error_msg.lower() or "credentials" in error_msg.lower():
                        print(f"  💡 This error usually means:")
                        print(f"     1. Invalid or missing Google Cloud credentials")
                        print(f"     2. Service account doesn't have required permissions")
                        print(f"     3. Vertex AI API is not enabled in your project")
                        print(f"  🔧 Please check:")
                        print(f"     - GOOGLE_APPLICATION_CREDENTIALS path in .env")
                        print(f"     - Service account has 'Vertex AI User' role")
                        print(f"     - Vertex AI API is enabled in Google Cloud Console")
                    elif "not found" in error_msg.lower() or "model" in error_msg.lower():
                        print(f"  💡 Model access issue:")
                        print(f"     - Gemini 2.5 Flash Image may not be available in {Config.GOOGLE_CLOUD_LOCATION}")
                        print(f"     - Try changing GOOGLE_CLOUD_LOCATION to 'us-central1' in .env")
                        print(f"     - Ensure the model is enabled for your project")
                    
                    continue
            
            except Exception as e:
                print(f"  ❌ Error generating image {img_idx + 1}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"\n{'='*80}")
        print(f"  📊 GENERATION SUMMARY")
        print(f"{'='*80}")
        print(f"  Requested: {num_images} images")
        print(f"  Generated: {len(generated_images)} images")
        print(f"{'='*80}\n")
        
        return {
            "images": generated_images,
            "size": size,
            "total": len(generated_images)
        }


# Global image service instance (will be initialized in app.py)
image_service = None
