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
