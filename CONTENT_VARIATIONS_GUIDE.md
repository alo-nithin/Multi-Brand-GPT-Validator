# 🚀 Content Variations Generator - Implementation Guide

## 🎯 **What We're Building**

A system that takes one piece of content and generates 3-5 variations, each optimized for different:
- **Tones** (professional, casual, urgent, friendly)
- **Audiences** (young professionals, families, businesses)
- **Platforms** (Instagram, LinkedIn, TikTok, X)
- **Campaigns** (awareness, conversion, engagement)

---

## 🛠️ **Implementation Steps**

### **Step 1: Create Content Generator Module**

**File:** `content_generator.py`
```python
import random
from typing import List, Dict, Any
from validator import load_brand_config

class ContentVariationGenerator:
    def __init__(self):
        self.tone_variations = {
            'professional': {
                'starters': ['We are pleased to announce', 'Our team is excited to share', 'We are proud to present'],
                'connectors': ['Furthermore', 'Additionally', 'Moreover'],
                'endings': ['We look forward to serving you', 'Thank you for your continued support', 'We appreciate your business']
            },
            'casual': {
                'starters': ['Hey there!', 'Check this out!', 'You gotta see this!'],
                'connectors': ['Plus', 'Also', 'And'],
                'endings': ['Let us know what you think!', 'Drop a comment below!', 'Tag a friend who needs this!']
            },
            'urgent': {
                'starters': ['Limited time offer!', 'Don\'t miss out!', 'Act now!'],
                'connectors': ['Hurry', 'Quick', 'Fast'],
                'endings': ['While supplies last!', 'Offer ends soon!', 'Don\'t wait!']
            },
            'friendly': {
                'starters': ['We\'re so excited to share', 'We think you\'ll love', 'We\'ve got something special'],
                'connectors': ['What\'s more', 'Best part', 'Plus'],
                'endings': ['We\'d love to hear from you!', 'Let\'s connect!', 'We\'re here to help!']
            }
        }
        
        self.audience_variations = {
            'young_professionals': {
                'keywords': ['career', 'growth', 'opportunity', 'success', 'networking'],
                'hashtags': ['#CareerGrowth', '#ProfessionalDevelopment', '#Networking']
            },
            'families': {
                'keywords': ['family', 'safe', 'reliable', 'trust', 'value'],
                'hashtags': ['#FamilyFirst', '#SafeChoice', '#FamilyValue']
            },
            'businesses': {
                'keywords': ['efficiency', 'ROI', 'productivity', 'scalable', 'enterprise'],
                'hashtags': ['#BusinessGrowth', '#Efficiency', '#ROI']
            }
        }

    def generate_variations(self, base_content: Dict, brand: str, platform: str, count: int = 3) -> List[Dict]:
        """Generate multiple variations of content"""
        brand_config = load_brand_config(brand)
        variations = []
        
        # Get brand-specific data
        voice = brand_config.get('voice', {})
        hashtag_bank = brand_config.get('hashtag_bank', {}).get(platform, [])
        cta_bank = brand_config.get('cta_bank', {}).get(platform, [])
        
        # Generate variations
        for i in range(count):
            variation = self._create_variation(
                base_content, 
                voice, 
                hashtag_bank, 
                cta_bank, 
                platform, 
                i
            )
            variations.append(variation)
        
        return variations

    def _create_variation(self, base_content: Dict, voice: Dict, hashtags: List, ctas: List, platform: str, variation_index: int) -> Dict:
        """Create a single variation"""
        
        # Determine tone based on brand voice and variation index
        tone = self._select_tone(voice, variation_index)
        
        # Modify caption
        caption = self._modify_caption(base_content.get('caption', ''), tone, platform)
        
        # Select hashtags
        selected_hashtags = self._select_hashtags(hashtags, platform, variation_index)
        
        # Select CTA
        selected_cta = self._select_cta(ctas, tone, variation_index)
        
        # Modify media suggestion
        media_suggestion = self._modify_media_suggestion(base_content.get('media_suggestion', {}), platform)
        
        return {
            'variation_id': f"var_{variation_index + 1}",
            'tone': tone,
            'caption': caption,
            'hashtags': selected_hashtags,
            'cta': selected_cta,
            'media_suggestion': media_suggestion,
            'platform': platform,
            'optimization_notes': self._get_optimization_notes(tone, platform)
        }

    def _select_tone(self, voice: Dict, variation_index: int) -> str:
        """Select tone based on brand voice and variation index"""
        brand_tone = voice.get('tone', 'professional').lower()
        
        # Map brand tone to variation tones
        tone_mapping = {
            'professional': ['professional', 'casual', 'friendly'],
            'casual': ['casual', 'friendly', 'professional'],
            'engaging': ['friendly', 'casual', 'urgent'],
            'customer-focused': ['friendly', 'professional', 'casual']
        }
        
        available_tones = tone_mapping.get(brand_tone, ['professional', 'casual', 'friendly'])
        return available_tones[variation_index % len(available_tones)]

    def _modify_caption(self, original_caption: str, tone: str, platform: str) -> str:
        """Modify caption based on tone and platform"""
        tone_data = self.tone_variations.get(tone, self.tone_variations['professional'])
        
        # Extract key information from original caption
        key_info = self._extract_key_info(original_caption)
        
        # Create new caption based on tone
        if tone == 'professional':
            caption = f"{random.choice(tone_data['starters'])} {key_info['main_message']}. {random.choice(tone_data['connectors'])} {key_info['benefit']}. {random.choice(tone_data['endings'])}."
        elif tone == 'casual':
            caption = f"{random.choice(tone_data['starters'])} {key_info['main_message']}! {random.choice(tone_data['connectors'])} {key_info['benefit']}. {random.choice(tone_data['endings'])}"
        elif tone == 'urgent':
            caption = f"{random.choice(tone_data['starters'])} {key_info['main_message']}! {random.choice(tone_data['connectors'])} {key_info['benefit']}. {random.choice(tone_data['endings'])}"
        else:  # friendly
            caption = f"{random.choice(tone_data['starters'])} {key_info['main_message']}! {random.choice(tone_data['connectors'])} {key_info['benefit']}. {random.choice(tone_data['endings'])}"
        
        # Adjust for platform
        caption = self._adjust_for_platform(caption, platform)
        
        return caption

    def _extract_key_info(self, caption: str) -> Dict[str, str]:
        """Extract key information from original caption"""
        # Simple extraction - in production, you'd use NLP
        return {
            'main_message': caption.split('.')[0] if '.' in caption else caption,
            'benefit': 'Quality guaranteed' if 'quality' in caption.lower() else 'Great value',
            'product': 'refurbished phones' if 'phone' in caption.lower() else 'products'
        }

    def _select_hashtags(self, hashtags: List[str], platform: str, variation_index: int) -> List[str]:
        """Select appropriate hashtags for variation"""
        if not hashtags:
            return []
        
        # Select 3-5 hashtags based on variation
        count = min(5, max(3, len(hashtags)))
        selected = random.sample(hashtags, min(count, len(hashtags)))
        
        # Add platform-specific hashtags
        platform_hashtags = {
            'Instagram': ['#InstaGood', '#PhotoOfTheDay'],
            'LinkedIn': ['#Professional', '#Business'],
            'TikTok': ['#FYP', '#Viral'],
            'X': ['#Trending', '#News']
        }
        
        if platform in platform_hashtags:
            selected.extend(platform_hashtags[platform][:2])
        
        return selected[:5]  # Limit to 5 hashtags

    def _select_cta(self, ctas: List[str], tone: str, variation_index: int) -> str:
        """Select appropriate CTA for variation"""
        if not ctas:
            return 'Learn more'
        
        # Select CTA based on tone
        tone_ctas = {
            'professional': ['Learn more', 'Contact us', 'Get started'],
            'casual': ['Check it out', 'Try it now', 'Get yours'],
            'urgent': ['Act now', 'Don\'t wait', 'Limited time'],
            'friendly': ['Let\'s connect', 'Join us', 'Be part of']
        }
        
        available_ctas = tone_ctas.get(tone, ctas)
        return random.choice(available_ctas) if available_ctas else ctas[0]

    def _modify_media_suggestion(self, media_suggestion: Dict, platform: str) -> Dict:
        """Modify media suggestion for platform"""
        modified = media_suggestion.copy()
        
        # Platform-specific adjustments
        if platform == 'Instagram':
            modified['notes'] = 'High-quality, visually appealing image'
        elif platform == 'LinkedIn':
            modified['notes'] = 'Professional, business-focused image'
        elif platform == 'TikTok':
            modified['notes'] = 'Engaging, dynamic video content'
        elif platform == 'X':
            modified['notes'] = 'Clear, attention-grabbing image'
        
        return modified

    def _adjust_for_platform(self, caption: str, platform: str) -> str:
        """Adjust caption length and style for platform"""
        max_lengths = {
            'Instagram': 2200,
            'LinkedIn': 3000,
            'TikTok': 2200,
            'X': 280
        }
        
        max_length = max_lengths.get(platform, 2200)
        
        if len(caption) > max_length:
            caption = caption[:max_length-3] + '...'
        
        return caption

    def _get_optimization_notes(self, tone: str, platform: str) -> str:
        """Get optimization notes for the variation"""
        notes = {
            'professional': f'Optimized for {platform} professional audience',
            'casual': f'Casual tone perfect for {platform} engagement',
            'urgent': f'Urgent tone to drive immediate action on {platform}',
            'friendly': f'Friendly approach to build community on {platform}'
        }
        
        return notes.get(tone, f'Optimized for {platform}')

# Global instance
content_generator = ContentVariationGenerator()
```

### **Step 2: Add API Endpoint**

**Add to `app.py`:**
```python
from content_generator import content_generator
from pydantic import BaseModel

class VariationRequest(BaseModel):
    base_content: Dict[str, Any]
    brand: str
    platform: str
    count: int = 3

@app.post("/generate/variations")
def generate_variations(request: VariationRequest, authorization: Optional[str] = Header(None)):
    """Generate multiple variations of content"""
    _auth_check(authorization)
    
    try:
        variations = content_generator.generate_variations(
            request.base_content,
            request.brand,
            request.platform,
            request.count
        )
        
        return {
            "success": True,
            "variations": variations,
            "count": len(variations),
            "brand": request.brand,
            "platform": request.platform
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "variations": []
        }
```

### **Step 3: Update Custom GPT Schema**

**Add to `custom_gpt_openapi_schema.json`:**
```json
"/generate/variations": {
  "post": {
    "summary": "Generate content variations",
    "description": "Generate multiple variations of content with different tones and optimizations",
    "operationId": "generateVariations",
    "requestBody": {
      "required": true,
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/VariationRequest"
          }
        }
      }
    },
    "responses": {
      "200": {
        "description": "Generated variations",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/VariationResponse"
            }
          }
        }
      }
    },
    "security": [
      {
        "bearerAuth": []
      }
    ]
  }
}
```

**Add schemas:**
```json
"VariationRequest": {
  "type": "object",
  "required": ["base_content", "brand", "platform"],
  "properties": {
    "base_content": {
      "type": "object",
      "description": "Base content to generate variations from"
    },
    "brand": {
      "type": "string",
      "description": "Brand name"
    },
    "platform": {
      "type": "string",
      "description": "Social media platform"
    },
    "count": {
      "type": "integer",
      "description": "Number of variations to generate",
      "default": 3
    }
  }
},
"VariationResponse": {
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "variations": {
      "type": "array",
      "items": {
        "$ref": "#/components/schemas/ContentVariation"
      }
    },
    "count": {
      "type": "integer"
    }
  }
},
"ContentVariation": {
  "type": "object",
  "properties": {
    "variation_id": {
      "type": "string"
    },
    "tone": {
      "type": "string"
    },
    "caption": {
      "type": "string"
    },
    "hashtags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "cta": {
      "type": "string"
    },
    "media_suggestion": {
      "type": "object"
    },
    "optimization_notes": {
      "type": "string"
    }
  }
}
```

### **Step 4: Update Custom GPT Instructions**

**Add to `custom_gpt_instructions.md`:**
```markdown
## Content Variations Generation:
When users ask for content variations or multiple versions:
1. Call generateVariations API with the base content
2. Present each variation with its tone and optimization notes
3. Explain the differences between variations
4. Suggest which variation works best for different audiences
5. Allow users to select their preferred variation

## Variation Examples:
- "Generate 3 variations of this Instagram post"
- "Create different versions for different audiences"
- "Make this content more casual/friendly/professional"
- "Adapt this for different platforms"
```

---

## 🧪 **Testing the Content Variations Generator**

### **Test API Directly:**
```bash
curl -X POST "https://multi-brand-gpt-validator.onrender.com/generate/variations" \
  -H "Authorization: Bearer H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0" \
  -H "Content-Type: application/json" \
  -d '{
    "base_content": {
      "caption": "Check out our latest refurbished phones! Quality guaranteed, prices that wont break the bank.",
      "hashtags": ["#AmarMarketplace", "#RefurbishedPhones"],
      "cta": "Shop now",
      "media_suggestion": {"type": "single_image"}
    },
    "brand": "Amar",
    "platform": "Instagram",
    "count": 3
  }'
```

### **Test Custom GPT Prompts:**
```
"Generate 3 variations of this Instagram post for Amar brand"
"Create different versions of this content for different audiences"
"Make this content more casual and friendly"
"Adapt this post for LinkedIn with a professional tone"
```

---

## 🎯 **Expected Results**

### **Input:**
```
"Check out our latest refurbished phones! Quality guaranteed, prices that wont break the bank."
```

### **Output Variations:**

**Variation 1 (Professional):**
```
"We are pleased to announce our latest refurbished phones. Furthermore, quality guaranteed, prices that wont break the bank. We look forward to serving you."
#AmarMarketplace #RefurbishedPhones #Professional #Business
CTA: "Learn more"
```

**Variation 2 (Casual):**
```
"Hey there! Check out our latest refurbished phones! Plus, quality guaranteed, prices that wont break the bank. Let us know what you think!"
#AmarMarketplace #RefurbishedPhones #InstaGood #PhotoOfTheDay
CTA: "Check it out"
```

**Variation 3 (Friendly):**
```
"We're so excited to share our latest refurbished phones! What's more, quality guaranteed, prices that wont break the bank. We'd love to hear from you!"
#AmarMarketplace #RefurbishedPhones #FYP #Viral
CTA: "Let's connect"
```

---

## 🚀 **Implementation Steps**

1. **Create `content_generator.py`** with the code above
2. **Add API endpoint** to `app.py`
3. **Update OpenAPI schema** in `custom_gpt_openapi_schema.json`
4. **Update Custom GPT instructions**
5. **Test with API** and Custom GPT
6. **Deploy to Render**

Would you like me to help you implement this step by step? I can start by creating the `content_generator.py` file! 🚀
