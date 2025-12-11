"""
Prompt generation controller
"""
from flask import request, jsonify
from services.ai_service import ai_service
from services.prompt_service import prompt_service


def generate_prompts():
    """Generate multiple prompt variations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        num_variations = data.get("num_variations", 3)
        params = data.get("params", {})
        
        print(f"\n📥 Received request data keys: {list(data.keys())}")
        print(f"📊 Total params received: {len(params)}")
        
        if not params.get("aspect_ratio"):
            return jsonify({"error": "aspect_ratio is required"}), 400
        
        # Validate aspect_ratio
        valid_aspect_ratios = [
            "instagram_post", "instagram_story", "facebook_post", 
            "linkedin_post", "pinterest", "twitter_post", 
            "youtube_thumbnail", "wide_banner"
        ]
        if params.get("aspect_ratio") not in valid_aspect_ratios:
            return jsonify({"error": f"Invalid aspect_ratio"}), 400
        
        # Check if user uploaded an image
        use_uploaded_image = params.get("use_uploaded_image", False)
        uploaded_image_base64 = params.get("uploaded_image", "")
        
        if use_uploaded_image and uploaded_image_base64:
            print(f"  🖼️  Image uploaded - analyzing with Claude...")
            image_description = ai_service.analyze_image_with_claude(uploaded_image_base64)
            if image_description:
                print(f"  ✓ Image analyzed")
                prompt_variations = prompt_service.create_prompts_from_image_and_data(
                    image_description, params, num_variations
                )
            else:
                return jsonify({"error": "Failed to analyze uploaded image"}), 500
        else:
            # Use AI-based prompt generation
            category = params.get("category", "general")
            print(f"  🎨 Generating AI-enhanced prompts...")
            prompt_variations = prompt_service.create_generic_prompts_for_custom_category(
                category, params, num_variations
            )
        
        # First, collect all variations with their lengths
        variations = []
        for i, prompt in enumerate(prompt_variations):
            preview = prompt[:200] + "..." if len(prompt) > 200 else prompt
            
            # Get description for this variation
            _, description = prompt_service.generate_variation_metadata(prompt, i + 1, params)
            
            variations.append({
                "id": i + 1,
                "prompt": prompt,
                "preview": preview,
                "length": len(prompt),
                "rating": 0,  # Will be calculated below
                "description": description
            })
        
        # Calculate ratings based on relative lengths
        # Create a mapping of length to rating
        lengths = [v["length"] for v in variations]
        sorted_lengths = sorted(lengths, reverse=True)
        
        # Create length-to-rating mapping
        length_to_rating = {}
        if len(sorted_lengths) >= 3:
            length_to_rating[sorted_lengths[0]] = 5  # Longest
            length_to_rating[sorted_lengths[1]] = 4  # Middle
            length_to_rating[sorted_lengths[2]] = 3  # Shortest
            # If more than 3, assign remaining ones rating 3
            for i in range(3, len(sorted_lengths)):
                length_to_rating[sorted_lengths[i]] = 3
        elif len(sorted_lengths) == 2:
            length_to_rating[sorted_lengths[0]] = 5  # Longest
            length_to_rating[sorted_lengths[1]] = 4  # Shorter
        elif len(sorted_lengths) == 1:
            length_to_rating[sorted_lengths[0]] = 5  # Only one
        
        # Assign ratings to each variation based on its length
        for variation in variations:
            variation["rating"] = length_to_rating[variation["length"]]
        
        return jsonify({
            "success": True,
            "total_variations": len(variations),
            "variations": variations,
            "params": params
        }), 200
    
    except Exception as e:
        print(f"❌ Error in generate_prompts: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
