"""
Prompt generation service
"""
from anthropic import Anthropic
from config.config import Config


class PromptService:
    """Service for generating and managing prompts"""
    
    @staticmethod
    def is_filled(value):
        """Check if a value is actually filled"""
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, list):
            return len(value) > 0 and any(PromptService.is_filled(item) for item in value)
        return bool(value)
    
    @staticmethod
    def create_base_prompt_from_description(params):
        """Create comprehensive base prompt from user-filled inputs"""
        # Extract and clean all possible parameters
        product_name = params.get("product_name", "").strip()
        category = params.get("category", "").strip()
        brand_name = params.get("brand_name", "").strip()
        
        # Text elements
        headline = params.get("headline", "").strip()
        subheadline = params.get("subheadline", "").strip()
        body_copy = params.get("body_copy", "").strip()
        tagline = params.get("tagline", "").strip()
        
        # Pricing
        price = params.get("price", "").strip()
        original_price = params.get("original_price", "").strip()
        discount_text = params.get("discount_text", "").strip()
        offer_label = params.get("offer_label", "").strip()
        
        # Features
        feature_list = params.get("feature_list", "")
        if isinstance(feature_list, list):
            feature_list = "\n".join([f"• {f.strip()}" for f in feature_list if PromptService.is_filled(f)])
        elif isinstance(feature_list, str):
            feature_list = feature_list.strip()
        
        # Contact information
        contact_info = params.get("contact_info", "").strip()
        phone = params.get("phone", "").strip()
        email = params.get("email", "").strip()
        website = params.get("website", "").strip()
        location = params.get("location", "").strip()
        
        # Call to action
        cta_text = params.get("cta_text", "").strip()
        
        # Visual preferences
        color_theme = params.get("color_theme", "").strip()
        background_color = params.get("background_color", "").strip()
        text_color = params.get("text_color", "").strip()
        
        # Build comprehensive base prompt
        base_parts = []
        
        # Introduction
        if PromptService.is_filled(category):
            base_parts.append(f"Create a clean, modern {category} advertising poster with a realistic and professional layout")
        elif PromptService.is_filled(product_name):
            base_parts.append(f"Create a clean, modern advertising poster for {product_name} with a realistic and professional layout")
        else:
            base_parts.append("Create a clean, modern advertising poster with a realistic and professional layout")
        
        # Brand/Product identification
        if PromptService.is_filled(brand_name):
            base_parts.append(f"Brand: {brand_name}")
        if PromptService.is_filled(product_name) and product_name != "product":
            base_parts.append(f"Product/Service: {product_name}")
        
        # Main headline
        if PromptService.is_filled(headline):
            base_parts.append(f"Main Headline (large, prominent): '{headline}'")
        
        # Subheadline
        if PromptService.is_filled(subheadline):
            base_parts.append(f"Subheadline: '{subheadline}'")
        
        # Body copy
        if PromptService.is_filled(body_copy):
            base_parts.append(f"Description: '{body_copy}'")
        
        # Features
        if PromptService.is_filled(feature_list):
            base_parts.append(f"Features Section (display exactly as written):\n{feature_list}")
        
        # Pricing information
        pricing_parts = []
        if PromptService.is_filled(price):
            pricing_parts.append(f"Price: '{price}'")
        if PromptService.is_filled(original_price):
            pricing_parts.append(f"Original Price (crossed out): '{original_price}'")
        if PromptService.is_filled(discount_text):
            pricing_parts.append(f"Discount/Offer: '{discount_text}'")
        if PromptService.is_filled(offer_label):
            pricing_parts.append(f"Offer Badge: '{offer_label}'")
        
        if pricing_parts:
            base_parts.append("Pricing Section: " + ", ".join(pricing_parts))
        
        # Contact information
        contact_parts = []
        if PromptService.is_filled(phone):
            contact_parts.append(f"Phone: '{phone}'")
        if PromptService.is_filled(email):
            contact_parts.append(f"Email: '{email}'")
        if PromptService.is_filled(website):
            contact_parts.append(f"Website: '{website}'")
        if PromptService.is_filled(location):
            contact_parts.append(f"Location: '{location}'")
        if PromptService.is_filled(contact_info):
            contact_parts.append(f"Additional Contact: '{contact_info}'")
        
        if contact_parts:
            base_parts.append("Contact Section: " + ", ".join(contact_parts))
        
        # Call to action
        if PromptService.is_filled(cta_text):
            base_parts.append(f"Call-to-Action Button: '{cta_text}'")
        
        # Tagline
        if PromptService.is_filled(tagline) and tagline != subheadline:
            base_parts.append(f"Tagline: '{tagline}'")
        
        # Design style preferences
        design_parts = []
        if PromptService.is_filled(color_theme):
            design_parts.append(f"color theme: {color_theme}")
        if PromptService.is_filled(background_color):
            design_parts.append(f"background: {background_color}")
        if PromptService.is_filled(text_color):
            design_parts.append(f"text color: {text_color}")
        
        if design_parts:
            base_parts.append("Design Style: " + ", ".join(design_parts))
        
        # Quality requirements - FULL BLEED, NO FRAMES, CONTENT SAFETY
        base_parts.append("Professional advertising poster composition featuring a confident, well-dressed professional man or woman in category-appropriate business attire standing naturally in the frame, visible from head down to at least the waist, occupying the right or left third of the image with sharp focus on their upper body and face, while the main product or service is prominently displayed in the remaining space, both subjects perfectly lit with studio lighting creating subtle rim light on edges, positioned against a clean gradient background transitioning from deep charcoal to midnight black, maintaining shallow depth of field with professional color grading, high-end commercial aesthetic, 4K quality, and ample negative space ensuring no elements overlap the model's face or shoulders, shot with full-frame camera perspective for authentic advertising photography feel. CRITICAL: Full-bleed edge-to-edge composition with NO frames, NO borders, NO mockups, NO device screens, NO containers - content must extend to all edges of the image canvas. CONTENT SAFETY: All content must be family-friendly, professional, and appropriate for all ages with modest, professional attire suitable for the category (business suit, medical scrubs, chef uniform, etc.) - absolutely NO revealing clothing, NO suggestive poses, NO 18+ content.")
        
        base_prompt = ". ".join(base_parts) + "."
        
        # Log what was included
        filled_fields = []
        if PromptService.is_filled(product_name): filled_fields.append("product_name")
        if PromptService.is_filled(category): filled_fields.append("category")
        if PromptService.is_filled(brand_name): filled_fields.append("brand_name")
        if PromptService.is_filled(headline): filled_fields.append("headline")
        if PromptService.is_filled(subheadline): filled_fields.append("subheadline")
        if PromptService.is_filled(body_copy): filled_fields.append("body_copy")
        if PromptService.is_filled(feature_list): filled_fields.append("features")
        if PromptService.is_filled(price): filled_fields.append("price")
        if PromptService.is_filled(cta_text): filled_fields.append("cta")
        
        print(f"  📝 Base prompt created from {len(filled_fields)} filled fields: {', '.join(filled_fields)}")
        print(f"  📝 Prompt length: {len(base_prompt)} chars")
        
        return base_prompt
    
    @staticmethod
    def create_prompts_from_image_and_data(image_description, params, num_variations=3):
        """Create prompts from image description + user placeholder data"""
        print(f"  📝 Creating prompts from image description + user data...")
        
        text_elements = []
        
        placeholder_mapping = {
            "headline": "headline text",
            "subheadline": "subheadline",
            "brand_name": "brand name",
            "product_name": "product name",
            "price": "price",
            "original_price": "original price",
            "discount_text": "discount offer",
            "offer_label": "offer badge",
            "cta_text": "call-to-action button",
            "feature_list": "features",
            "body_copy": "description",
            "contact_info": "contact information",
            "location": "location",
            "phone_color": "phone color",
            "product_color": "product color",
            "color_theme": "color theme",
            "background_color": "background color",
            "text_color": "text color",
            "accent_color": "accent color"
        }
        
        for key, label in placeholder_mapping.items():
            value = params.get(key)
            if value and str(value).strip():
                text_elements.append(f"{label} '{value}'")
        
        all_text = ", ".join(text_elements) if text_elements else ""
        
        print(f"  📝 User provided {len(text_elements)} text elements")
        
        variations = []
        
        if all_text:
            variations.append(
                f"{image_description} "
                f"IMPORTANT: Add these text overlays to the image: {all_text}. "
                f"Make sure all text is clearly visible and readable."
            )
            
            variations.append(
                f"Recreate this exact visual: {image_description}. "
                f"Include these text elements prominently: {all_text}. "
                f"Text should be clear and legible."
            )
            
            variations.append(
                f"{image_description} "
                f"Add the following text overlays in appropriate positions: {all_text}. "
                f"Ensure text is visible, well-positioned, and matches the image style."
            )
        else:
            for i in range(num_variations):
                variations.append(f"{image_description}")
        
        variations = variations[:num_variations]
        
        while len(variations) < num_variations:
            variations.append(
                f"Exact visual recreation: {image_description}. "
                f"Text overlays to include: {all_text}. "
                f"Make text prominent and readable."
            )
        
        return variations
    
    @staticmethod
    def generate_variation_metadata(prompt, variation_number, params, all_prompt_lengths=None):
        """Generate rating and description for a prompt variation based on relative prompt length"""
        # Simple descriptions: Person position | Content position | Visual style
        variation_styles = {
            1: {
                "description": "Person: Right | Content: Left | Warm lighting, beige gradient",
            },
            2: {
                "description": "Person: Left | Content: Right | Dramatic lighting, dark gradient",
            },
            3: {
                "description": "Person: Left | Content: Right | Cool lighting, light gradient",
            }
        }
        
        # Get style info for this variation (cycle through if more than 3)
        style_key = ((variation_number - 1) % 3) + 1
        style_info = variation_styles[style_key]
        description = style_info["description"]
        
        # Calculate rating based on RELATIVE prompt character length
        prompt_length = len(prompt)
        
        if all_prompt_lengths and len(all_prompt_lengths) > 1:
            # Relative rating: longest gets 5 stars, others proportionally lower
            max_length = max(all_prompt_lengths)
            min_length = min(all_prompt_lengths)
            
            if max_length == min_length:
                # All prompts same length
                rating = 4
            else:
                # Calculate percentage of max length
                length_ratio = (prompt_length - min_length) / (max_length - min_length)
                
                # Map to 5-star scale (3-5 stars)
                # Longest = 5, shortest = 3, middle = 4
                if length_ratio >= 0.9:
                    rating = 5  # Top 10% - Longest
                elif length_ratio >= 0.5:
                    rating = 4  # Middle 40% - Medium
                else:
                    rating = 3  # Bottom 50% - Shortest
        else:
            # Fallback if no comparison data
            rating = 4
        
        return rating, description
    
    @staticmethod
    def create_generic_prompts_for_custom_category(category, params, num_variations=3):
        """Create advertising prompts with Claude AI enhancement and diverse variations"""
        print(f"\n🎨 Creating prompts for {category}...")
        
        print(f"  📝 Step 1: Creating base prompt from product description...")
        base_prompt = PromptService.create_base_prompt_from_description(params)
        
        print(f"  🤖 Step 2: Enhancing with Claude AI for {num_variations} distinct variations...")
        
        # Define variation styles - 2 men, 1 woman with category-appropriate attire
        # Attire adapts to category while maintaining professionalism
        variation_styles = [
            {
                "number": 1,
                "model": "confident professional man in category-appropriate business attire",
                "position": "right third of the frame",
                "product_position": "left side"
            },
            {
                "number": 2,
                "model": "well-dressed professional man in category-appropriate formal attire",
                "position": "left third of the frame",
                "product_position": "right side"
            },
            {
                "number": 3,
                "model": "confident professional woman in elegant category-appropriate business attire",
                "position": "left third of the frame",
                "product_position": "right side"
            }
        ]
        
        enhanced_variations = []
        
        for i in range(num_variations):
            try:
                # Get style for this variation (cycle through if more than 3)
                style = variation_styles[i % len(variation_styles)]
                
                print(f"    🤖 Enhancing variation {i+1}/{num_variations} with Claude AI...")
                
                # Create enhancement instruction for Claude
                enhancement_instruction = f"""You are an expert at creating Google Imagen 4.0 prompts for advertising photography.

TASK: Convert this base advertising prompt into a professional, detailed Imagen 4.0 prompt (MAX 1800 characters).

CRITICAL REQUIREMENTS:
1. COPY ALL USER TEXT EXACTLY - do not change any headlines, prices, features, or contact info
2. Keep total output under 1800 characters
3. Use EXACTLY these specifications for VARIATION {style['number']}:
   - Model: {style['model']}
   - Model Position: {style['position']}
   - Product Placement: {style['product_position']}
4. FULL-BLEED COMPOSITION: Content must extend edge-to-edge with NO frames, NO borders, NO mockups, NO device screens, NO containers around the image
5. CONTENT SAFETY: All content must be family-friendly, professional, and appropriate for all ages (no 18+ content, no suggestive poses, no revealing clothing)
6. ATTIRE GUIDELINES: Dress the model appropriately for the category (e.g., medical scrubs for healthcare, chef uniform for food, business suit for corporate, casual professional for tech)

YOUR CREATIVE FREEDOM (make each variation unique):
- Choose lighting style (warm/dramatic/natural/etc)
- Choose background colors and gradients
- Choose overall aesthetic (minimalist/bold/elegant/etc)
- Add photography details (depth of field, camera angle, etc)
- Make this variation DISTINCTLY DIFFERENT from others

FORMAT:
Start with: "{style['model']} positioned on {style['position']}, product on {style['product_position']}."
Then add all text elements with EXACT user text.
Then add your creative lighting, background, and aesthetic choices.
End with: "Full-bleed edge-to-edge composition, no frames or borders, content extends to all edges."

BASE PROMPT (copy all text EXACTLY):
{base_prompt}

OUTPUT ENHANCED PROMPT (under 1800 chars, exact text, creative styling):"""

                client = Anthropic(
                    api_key=Config.CLAUDE_API_KEY,
                    base_url=Config.CLAUDE_ENDPOINT
                )
                
                message = client.messages.create(
                    model=Config.CLAUDE_DEPLOYMENT,
                    messages=[{"role": "user", "content": enhancement_instruction}],
                    max_tokens=2000,
                    temperature=0.7 + (i * 0.1)  # Increase temperature for more variation
                )
                
                enhanced = message.content[0].text.strip()
                enhanced_variations.append(enhanced)
                print(f"    ✓ Variation {i+1} enhanced by Claude ({len(enhanced)} chars)")
                
            except Exception as e:
                print(f"    ⚠️  Claude enhancement failed: {e}")
                # Fallback: use base prompt with simple style modification
                style = variation_styles[i % len(variation_styles)]
                fallback = (
                    f"{style['model']} positioned on {style['position']}, "
                    f"product on {style['product_position']}. {base_prompt}"
                )
                enhanced_variations.append(fallback)
                print(f"    ⚠️  Using fallback for variation {i+1}")
        
        print(f"  ✅ Step 3: {len(enhanced_variations)} AI-enhanced variations ready")
        return enhanced_variations


# Global prompt service instance
prompt_service = PromptService()
