# Content Safety Guidelines - December 2025

## Overview

All generated images follow strict content safety guidelines to ensure family-friendly, professional content appropriate for all ages.

## Model Distribution

### 2 Men, 1 Woman

**Variation 1**: Professional Man (Right Side)  
**Variation 2**: Professional Man (Left Side)  
**Variation 3**: Professional Woman (Left Side)

This distribution ensures:
- Gender diversity
- Professional representation
- Consistent quality across variations

## Category-Appropriate Attire

Models are dressed according to the product/service category:

| Category | Attire Example |
|----------|----------------|
| **Healthcare** | Medical scrubs, lab coat, professional medical attire |
| **Food & Restaurant** | Chef uniform, apron, professional kitchen attire |
| **Corporate/Business** | Business suit, formal business attire |
| **Technology** | Smart casual, business casual, modern professional |
| **Education** | Professional academic attire, smart casual |
| **Real Estate** | Business suit, professional formal attire |
| **Finance** | Formal business suit, conservative professional |
| **Retail** | Brand-appropriate uniform, professional casual |
| **Travel & Tourism** | Smart casual, professional travel attire |
| **Fitness** | Professional athletic wear, trainer attire |

## Content Safety Rules

### ✅ Always Include

- Professional, modest attire
- Family-friendly poses
- Appropriate for all ages
- Business-appropriate settings
- Respectful representation
- Category-appropriate clothing

### ❌ Never Include

- Revealing clothing
- Suggestive poses
- 18+ content
- Inappropriate attire
- Unprofessional settings
- Offensive imagery

## Implementation

### Base Prompt Safety

Every prompt includes:

```
CONTENT SAFETY: All content must be family-friendly, professional, and 
appropriate for all ages with modest, professional attire suitable for 
the category (business suit, medical scrubs, chef uniform, etc.) - 
absolutely NO revealing clothing, NO suggestive poses, NO 18+ content.
```

### Claude AI Instructions

Claude receives explicit guidelines:

```
5. CONTENT SAFETY: All content must be family-friendly, professional, 
   and appropriate for all ages (no 18+ content, no suggestive poses, 
   no revealing clothing)

6. ATTIRE GUIDELINES: Dress the model appropriately for the category 
   (e.g., medical scrubs for healthcare, chef uniform for food, 
   business suit for corporate, casual professional for tech)
```

### Variation Styles

```python
variation_styles = [
    {
        "model": "confident professional man in category-appropriate business attire",
        "position": "right third of the frame",
    },
    {
        "model": "well-dressed professional man in category-appropriate formal attire",
        "position": "left third of the frame",
    },
    {
        "model": "confident professional woman in elegant category-appropriate business attire",
        "position": "left third of the frame",
    }
]
```

## Examples by Category

### Healthcare Ad
```
Model: Professional man in medical scrubs and lab coat
Setting: Clean medical environment
Attire: Full coverage, professional medical uniform
```

### Food & Restaurant Ad
```
Model: Professional man in chef uniform with apron
Setting: Professional kitchen or restaurant
Attire: Complete chef attire, professional appearance
```

### Corporate/Business Ad
```
Model: Professional woman in elegant business suit
Setting: Modern office or professional environment
Attire: Full business suit, professional and modest
```

### Technology Ad
```
Model: Professional man in smart casual business attire
Setting: Modern tech environment
Attire: Business casual, professional and appropriate
```

## AI Model Safeguards

### Gemini 2.5 Flash Image
- Built-in content safety filters
- Automatic rejection of inappropriate content
- Family-friendly output by default

### Azure FLUX
- Content moderation enabled
- Safety filters active
- Professional output standards

## Monitoring & Compliance

### Automatic Checks
- AI models have built-in safety filters
- Prompts include explicit safety instructions
- Category-appropriate attire specified

### Manual Review
- Users can report inappropriate content
- Admin can review flagged images
- Continuous improvement of guidelines

## User Responsibilities

### Users Should
- ✅ Provide appropriate product descriptions
- ✅ Use professional language
- ✅ Request family-friendly content
- ✅ Report any inappropriate outputs

### Users Should Not
- ❌ Request revealing or suggestive content
- ❌ Use inappropriate language
- ❌ Attempt to bypass safety filters
- ❌ Generate 18+ content

## Enforcement

### Prompt Level
- Safety instructions in every prompt
- Category-appropriate attire specified
- Professional standards enforced

### AI Model Level
- Built-in content filters
- Automatic rejection of inappropriate requests
- Safety-first generation

### Application Level
- Clear usage guidelines
- User education
- Reporting mechanisms

## Benefits

### For Users
- ✅ Safe, professional content
- ✅ Appropriate for all audiences
- ✅ Brand-safe imagery
- ✅ No moderation concerns

### For Business
- ✅ Compliant with advertising standards
- ✅ Family-friendly brand image
- ✅ Professional reputation
- ✅ Reduced liability

### For Society
- ✅ Respectful representation
- ✅ Appropriate for all ages
- ✅ Professional standards
- ✅ Positive role models

## Technical Implementation

### Prompt Service (prompt_service.py)

```python
# Base prompt includes safety guidelines
base_parts.append("...CONTENT SAFETY: All content must be family-friendly...")

# Claude instructions include safety requirements
"5. CONTENT SAFETY: All content must be family-friendly..."
"6. ATTIRE GUIDELINES: Dress the model appropriately for the category..."

# Variation styles specify category-appropriate attire
"model": "confident professional man in category-appropriate business attire"
```

### Image Service (image_service.py)

Both AI models (Gemini and Azure FLUX) receive prompts with:
- Explicit safety instructions
- Category-appropriate attire specifications
- Professional standards requirements

## Updates & Maintenance

### Regular Reviews
- Monitor generated content
- Update guidelines as needed
- Improve safety instructions
- Refine category mappings

### User Feedback
- Collect user reports
- Address concerns promptly
- Improve safety measures
- Enhance guidelines

## Summary

**Model Distribution**: 2 Men, 1 Woman  
**Attire**: Category-appropriate professional clothing  
**Content**: Family-friendly, appropriate for all ages  
**Safety**: Multiple layers of protection  
**Compliance**: Advertising standards compliant  

All generated images are safe, professional, and appropriate for business use! 🛡️

---

**Last Updated**: December 10, 2025  
**Status**: ✅ Active  
**Compliance**: Family-friendly, all-ages appropriate
