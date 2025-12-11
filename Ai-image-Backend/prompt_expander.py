"""
Social Media Ad Generator - Prompt Expander

Minimal version - only contains what's actually used by app.py
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


class AdvancedAdGenerator:
    """
    Generate social media ad prompts using AI enhancement.
    Provides Claude AI client and configuration options for the frontend.
    """

    def __init__(self, api_key=None, endpoint=None, deployment_name=None):
        self.api_key = api_key or os.getenv("AZURE_CLAUDE_API_KEY")
        self.endpoint = endpoint or os.getenv("AZURE_CLAUDE_ENDPOINT")
        self.deployment_name = deployment_name or os.getenv("CLAUDE_DEPLOYMENT_NAME", "claude-opus-4-1")
        
        if not self.api_key or not self.endpoint:
            raise ValueError("API key and endpoint must be provided")
        
        # Initialize Claude AI client
        self.client = Anthropic(
            api_key=self.api_key,
            base_url=self.endpoint
        )

        # Configuration options for frontend dropdowns
        self.ad_objectives = {
            "brand_awareness": "Brand Awareness",
            "sales_boost": "Sales Boost",
            "discount_promotion": "Discount Promotion",
            "product_launch": "Product Launch",
            "event_promotion": "Event Promotion"
        }

        self.visual_styles = {
            "minimal": "Minimal & Clean",
            "premium": "Premium & Luxury",
            "modern": "Modern & Sleek",
            "bold": "Bold & Vibrant",
            "cinematic": "Cinematic"
        }

        self.lighting_styles = {
            "studio": "Studio Lighting",
            "natural": "Natural Light",
            "dramatic": "Dramatic Lighting",
            "soft_diffused": "Soft Diffused",
            "golden_hour": "Golden Hour"
        }

        self.backgrounds = {
            "solid_color": "Solid Color",
            "gradient": "Gradient",
            "studio_white": "Studio White",
            "studio_black": "Studio Black",
            "blurred_depth": "Blurred Background"
        }

        self.product_angles = {
            "front_view": "Front View",
            "45_degree": "45° Angle",
            "top_view": "Top View",
            "floating": "Floating"
        }

        self.cta_options = {
            "shop_now": "Shop Now",
            "order_now": "Order Now",
            "learn_more": "Learn More",
            "get_started": "Get Started",
            "claim_offer": "Claim Offer"
        }

    def generate_multiple_prompt_variations(self, params, num_variations=3):
        """
        Generate multiple prompt variations using parameter-based method.
        This is a fallback method when no category is provided.
        
        Returns list of prompt strings.
        """
        print(f"\n🎨 Generating {num_variations} prompt variations...")
        
        product_name = params.get("product_name", "product")
        headline = params.get("headline", "")
        price = params.get("price", "")
        discount_text = params.get("discount_text", "")
        cta_text = params.get("cta_text", "Shop Now")
        
        variations = []
        
        # Create simple base prompts with different styles
        styles = [
            "Modern clean design with studio lighting and gradient background",
            "Bold vibrant style with high contrast and dynamic composition",
            "Premium luxury aesthetic with soft lighting and minimalist layout"
        ]
        
        for i in range(num_variations):
            style = styles[i % len(styles)]
            
            # Build prompt
            prompt_parts = [f"Professional advertising poster for {product_name}"]
            
            if headline:
                prompt_parts.append(f"Main headline: '{headline}'")
            if price:
                prompt_parts.append(f"Price: {price}")
            if discount_text:
                prompt_parts.append(f"Special offer: {discount_text}")
            if cta_text:
                prompt_parts.append(f"Call-to-action: '{cta_text}'")
            
            prompt_parts.append(style)
            
            prompt = ". ".join(prompt_parts) + "."
            variations.append(prompt)
            print(f"  ✓ Variation {i+1} created ({len(prompt)} chars)")
        
        return variations
