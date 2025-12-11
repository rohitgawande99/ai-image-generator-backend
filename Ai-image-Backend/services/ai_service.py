"""
AI service for image analysis and prompt generation
"""
import os
from anthropic import Anthropic
from config.config import Config
from prompt_expander import AdvancedAdGenerator
from utils.image_utils import detect_image_type, convert_image_to_png

# Import Google GenAI for Vertex AI
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️  Google GenAI SDK not installed. Run: pip install google-genai")


class AIService:
    """Service for AI-related operations"""
    
    def __init__(self):
        # Initialize Ad Generator
        self.ad_generator = AdvancedAdGenerator(Config.CLAUDE_API_KEY)
        
        # Initialize Google GenAI client for Gemini 2.5 Flash Image
        self.genai_client = None
        self.image_model_name = "publishers/google/models/gemini-2.5-flash-image"
        
        if GENAI_AVAILABLE:
            try:
                # Set credentials path
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = Config.GOOGLE_APPLICATION_CREDENTIALS
                
                # Initialize GenAI client with Vertex AI
                self.genai_client = genai.Client(
                    vertexai=True,
                    project=Config.GOOGLE_CLOUD_PROJECT,
                    location=Config.GOOGLE_CLOUD_LOCATION
                )
                
                print(f"✅ Google GenAI initialized with Gemini 2.5 Flash Image")
                print(f"   Project: {Config.GOOGLE_CLOUD_PROJECT}")
                print(f"   Location: {Config.GOOGLE_CLOUD_LOCATION}")
                print(f"   Model: {self.image_model_name}")
            except Exception as e:
                print(f"⚠️  Google GenAI initialization error: {e}")
                self.genai_client = None
        else:
            print("⚠️  Google GenAI SDK not available")
    
    def analyze_image_with_claude(self, image_base64):
        """Analyze uploaded image using Claude Vision API"""
        try:
            print(f"  🤖 Calling Claude Vision API for detailed analysis...")
            
            media_type = detect_image_type(image_base64)
            print(f"  📷 Detected image type: {media_type}")
            
            analysis_prompt = """You are an expert at describing images for AI image generation. Analyze this image in EXTREME detail to recreate it EXACTLY.

Describe EVERY visual element you see:

1. MAIN SUBJECT:
   - What is it? (product type, model, features)
   - Exact position (centered, left, right, top, bottom, angle)
   - Size relative to frame (fills 50%, 70%, etc.)
   - Orientation (front view, 3/4 angle, side view, tilted)
   - Physical details (shape, materials, textures, finish - glossy/matte)

2. COLORS - BE SPECIFIC:
   - Exact color names (not just "blue" but "deep navy blue", "electric cyan")
   - Color of main subject
   - Background colors (solid, gradient - specify start and end colors)
   - Accent colors
   - Color temperature (warm/cool)

3. LIGHTING - EXACT DETAILS:
   - Light source position (top, front, side, back)
   - Light quality (soft diffused, hard direct, studio, natural)
   - Highlights location and intensity
   - Shadow direction, softness, and darkness
   - Rim lighting, edge lighting, glow effects

4. BACKGROUND - PRECISE:
   - Type (solid color, gradient, pattern, environment)
   - If gradient: direction (top to bottom, left to right, radial) and exact colors
   - Texture (smooth, grainy, blurred)
   - Any background elements or shapes

5. COMPOSITION:
   - Subject placement (rule of thirds, centered, golden ratio)
   - Negative space distribution
   - Depth (flat, 3D, layered)
   - Perspective (straight on, from above, from below)

6. SURFACE & MATERIALS:
   - Reflections (where, how strong, what's reflected)
   - Surface the subject sits on (reflective, matte, floating, pedestal)
   - Material properties (metal, plastic, glass, fabric)
   - Texture details (smooth, rough, brushed, polished)

7. STYLE & EFFECTS:
   - Photography style (product photography, lifestyle, artistic)
   - Post-processing (color grading, contrast, saturation)
   - Special effects (glow, particles, bokeh, lens flare)
   - Overall aesthetic (minimalist, bold, luxury, tech, vintage)

8. TECHNICAL SPECS:
   - Depth of field (everything sharp, background blur, how much blur)
   - Focus point
   - Image quality (crisp, soft, grain)
   - Aspect ratio feel

CRITICAL: Describe this image so precisely that someone could recreate it EXACTLY without seeing it. Include measurements, percentages, exact color names, specific positions. Be extremely detailed - aim for 8-12 sentences covering every visual aspect.

IGNORE any text in the image - describe only the visual elements, composition, colors, lighting, and style."""

            message = self.ad_generator.client.messages.create(
                model=self.ad_generator.deployment_name,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": analysis_prompt
                            }
                        ]
                    }
                ]
            )
            
            description = message.content[0].text.strip()
            print(f"  ✓ Claude analysis complete")
            return description
            
        except Exception as e:
            print(f"  ⚠️  Claude image analysis failed: {e}")
            return ""
    
    def analyze_image_for_extraction(self, image_base64):
        """Analyze image and extract text fields and visual description"""
        try:
            print(f"\n🖼️  Analyzing uploaded image with Claude Vision...")
            
            # Clean base64 data
            image_base64 = image_base64.strip()
            
            if ',' in image_base64 and image_base64.startswith('data:'):
                print(f"  🧹 Removing data URL prefix...")
                image_base64 = image_base64.split(',', 1)[1]
            
            image_base64 = image_base64.replace('\n', '').replace('\r', '').replace(' ', '')
            
            print(f"  📊 Base64 length: {len(image_base64)} characters")
            
            # Detect image type
            media_type = detect_image_type(image_base64)
            print(f"  📷 Detected image type: {media_type}")
            
            # Check if format is supported by Claude
            claude_supported_formats = ["image/jpeg", "image/png", "image/gif", "image/webp"]
            
            if media_type not in claude_supported_formats:
                print(f"  ⚠️  {media_type} is not supported by Claude Vision API")
                print(f"  🔄 Converting to PNG...")
                
                converted_base64, converted_type = convert_image_to_png(image_base64)
                
                if converted_base64:
                    image_base64 = converted_base64
                    media_type = converted_type
                    print(f"  ✅ Successfully converted to {media_type}")
                else:
                    raise Exception(f"Could not convert {media_type} to supported format")
            
            # Create comprehensive analysis prompt
            analysis_prompt = """You are an expert at analyzing advertising posters. Analyze this image and extract ALL information.

OUTPUT FORMAT (JSON):
{
  "visual_description": "Detailed description of the visual scene (person, product, background, lighting, composition) - 3-4 sentences",
  "headline": "Main headline text (if visible)",
  "subheadline": "Subheadline text (if visible)",
  "body_copy": "Body text or description (if visible)",
  "price": "Price (if visible)",
  "original_price": "Original/crossed-out price (if visible)",
  "discount_text": "Discount or offer text (if visible)",
  "offer_label": "Badge text like 'SALE', 'NEW', 'LIMITED' (if visible)",
  "phone": "Phone number (if visible)",
  "email": "Email address (if visible)",
  "website": "Website URL (if visible)",
  "location": "Location or address (if visible)",
  "cta_text": "Call-to-action button text (if visible)",
  "brand_name": "Brand or company name (if visible)",
  "features": ["Feature 1", "Feature 2", "Feature 3"],
  "color_theme": "Main colors used (e.g., 'Gold, Navy Blue')",
  "background_color": "Background color or gradient",
  "category": "Best category: Real Estate, Mobile, Fashion, Food, Education, Travel, or General"
}

INSTRUCTIONS:
1. Extract ALL visible text exactly as written
2. Describe the visual scene in detail (person, product, background, lighting)
3. Identify the main colors and design style
4. Suggest the best category for this type of ad
5. If a field has no visible text, use empty string ""
6. For features, extract bullet points or key features if visible

Be thorough - extract every piece of text you can see!"""

            # Call Claude Vision API
            message = self.ad_generator.client.messages.create(
                model=self.ad_generator.deployment_name,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": analysis_prompt
                            }
                        ]
                    }
                ]
            )
            
            response_text = message.content[0].text.strip()
            print(f"  ✅ Claude analysis complete")
            
            # Extract JSON from response
            import json
            import re
            
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                json_str = json_match.group(0)
                analysis_data = json.loads(json_str)
            else:
                analysis_data = json.loads(response_text)
            
            print(f"  ✓ Extracted data from image")
            print(f"  📊 Found {len([v for v in analysis_data.values() if v])} filled fields")
            
            return analysis_data
            
        except Exception as e:
            print(f"❌ Error in analyze_image_for_extraction: {e}")
            raise
    
    def autofill_fields_with_ai(self, product_description, category="", brand_name=""):
        """Use Claude AI to auto-fill form fields"""
        try:
            print(f"\n🤖 Auto-filling fields with Claude AI...")
            print(f"  Product: {product_description}")
            print(f"  Category: {category}")
            print(f"  Brand: {brand_name}")
            
            autofill_prompt = f"""You are a professional advertising copywriter. Generate SHORT, CONCISE content for an advertising poster. Keep ALL text very brief for better AI image generation.

PRODUCT INFORMATION:
- Description: {product_description}
- Category: {category if category else "general"}
- Brand: {brand_name if brand_name else "not specified"}

CRITICAL: Keep ALL text VERY SHORT (3-4 words maximum per field) for optimal AI image text rendering!

Generate these fields with MINIMAL text:

1. HEADLINE: 2-4 words max (e.g., "Master AI Development", "Luxury Living Awaits")
2. SUBHEADLINE: 3-5 words max (e.g., "Learn Build Deploy", "Premium Dubai Residences")
3. BODY_COPY: 5-8 words max (e.g., "Build AI agents like a pro")
4. FEATURES: 3-4 features, each 2-3 words (e.g., "24/7 Support", "Cloud Ready", "Fast Setup")
5. PRICE: Just the number with currency (e.g., "$497", "AED 2,500,000")
6. ORIGINAL_PRICE: Just the number with currency (e.g., "$697", "AED 3,000,000")
7. DISCOUNT_TEXT: 2-3 words (e.g., "Save $200", "30% Off")
8. OFFER_LABEL: 1-2 words (e.g., "SALE", "NEW", "LIMITED")
9. PHONE: Standard format (e.g., "+1 555 1234", "+971 4 888 9500")
10. EMAIL: Simple email (e.g., "info@company.com")
11. WEBSITE: Simple URL (e.g., "www.company.com")
12. LOCATION: City/Area only (e.g., "Dubai Marina", "New York")
13. CTA_TEXT: 1-2 words (e.g., "Buy Now", "Learn More", "Contact Us")
14. TAGLINE: 2-4 words (e.g., "Excellence Delivered Daily", "Your Success Partner")
15. COLOR_THEME: 2 colors (e.g., "Gold, Navy Blue")
16. BACKGROUND_COLOR: 1 color or simple gradient (e.g., "Dark Blue", "Navy to Black")

OUTPUT FORMAT (JSON):
{{
  "headline": "...",
  "subheadline": "...",
  "body_copy": "...",
  "features": ["...", "...", "...", "..."],
  "price": "...",
  "original_price": "...",
  "discount_text": "...",
  "offer_label": "...",
  "phone": "...",
  "email": "...",
  "website": "...",
  "location": "...",
  "cta_text": "...",
  "tagline": "...",
  "color_theme": "...",
  "background_color": "..."
}}

Generate SHORT, CONCISE content now (remember: 2-4 words per field!):"""

            client = Anthropic(
                api_key=Config.CLAUDE_API_KEY,
                base_url=Config.CLAUDE_ENDPOINT
            )
            
            message = client.messages.create(
                model=Config.CLAUDE_DEPLOYMENT,
                messages=[{"role": "user", "content": autofill_prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            response_text = message.content[0].text.strip()
            print(f"  ✓ Claude response received")
            
            import json
            import re
            
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                json_str = json_match.group(0)
                autofill_data = json.loads(json_str)
            else:
                autofill_data = json.loads(response_text)
            
            print(f"  ✓ Auto-fill data generated successfully")
            
            return autofill_data
            
        except Exception as e:
            print(f"❌ Error in autofill_fields_with_ai: {e}")
            raise
    
    def get_config_options(self):
        """Get configuration options for frontend"""
        return {
            "ad_objectives": self.ad_generator.ad_objectives,
            "visual_styles": self.ad_generator.visual_styles,
            "lighting_styles": self.ad_generator.lighting_styles,
            "backgrounds": self.ad_generator.backgrounds,
            "product_angles": self.ad_generator.product_angles,
            "cta_options": self.ad_generator.cta_options,
            "aspect_ratios": {
                "instagram_post": "Instagram Post (1:1)",
                "instagram_story": "Instagram Story (9:16)",
                "facebook_post": "Facebook Post (1:1)",
                "youtube_thumbnail": "YouTube Thumbnail (16:9)"
            }
        }


# Global AI service instance
ai_service = AIService()
