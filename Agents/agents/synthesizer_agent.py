# agents/synthesizer_agent.py
"""
🎨 The Content Synthesizer Agent (Storytelling Image Focus)
- Creates social media posts from storytelling images
- Formats e-commerce content to emphasize emotional connection
- Uses storytelling images instead of product photos
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentSynthesizer:
    """
    The Content Synthesizer Agent (Storytelling Image Focus)
    Goal: Create marketing assets that emphasize the artisan's story and cultural heritage
    """
    
    def __init__(self):
        # Load fonts (Indian market specific)
        try:
            self.font_large = ImageFont.truetype("arialbd.ttf", 48)
            self.font_medium = ImageFont.truetype("arial.ttf", 36)
            self.font_small = ImageFont.truetype("arial.ttf", 28)
        except:
            # Fallback to default font
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
    
    def create_story_post(self, storytelling_dict, image_path: str, output_path: str = "story_post.jpg") -> str:
        """Create social media post focused on the artisan's story with storytelling image"""
        logger.info("🖼️ Creating story-focused social post with storytelling image...")
        
        # Open the storytelling image
        img = Image.open(image_path)
        width, height = img.size
        
        # Resize to Instagram post dimensions if needed
        if width != 1080 or height != 1350:
            img = img.resize((1080, 1080))
            width, height = 1080, 1080
        
        # Create a new image with space for text at the bottom
        canvas = Image.new('RGB', (width, height + 300), (25, 25, 75))  # Deep blue background
        canvas.paste(img, (0, 0))
        
        draw = ImageDraw.Draw(canvas)
        
        # Add decorative border (simplified Indian pattern)
        border_color = (255, 215, 0)  # Gold
        for i in range(5):
            draw.rectangle([i, i, width-i-1, height-i-1], outline=border_color, width=2)
        
        # Add story title
        title = storytelling_dict["story_title"]
        title_width = draw.textlength(title, font=self.font_large)
        x = (width - title_width) / 2
        draw.text((x, height + 30), title, font=self.font_large, fill=(255, 215, 0))  # Gold color
        
        # Add emotional theme
        theme = f"Theme: {storytelling_dict['emotional_theme']}"
        theme_width = draw.textlength(theme, font=self.font_medium)
        x = (width - theme_width) / 2
        draw.text((x, height + 90), theme, font=self.font_medium, fill=(255, 255, 255))
        
        # Add story elements
        margin = 80
        max_width = width - (2 * margin)
        y = height + 140
        
        for element in storytelling_dict["image_prompts"]:
            # Split long elements into multiple lines
            words = element.split()
            current_line = []
            lines = []
            
            for word in words:
                test_line = " ".join(current_line + [word])
                if draw.textlength(test_line, font=self.font_medium) <= max_width:
                    current_line.append(word)
                else:
                    lines.append(" ".join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(" ".join(current_line))
            
            # Draw each line
            for line in lines:
                text_width = draw.textlength(line, font=self.font_medium)
                x = (width - text_width) / 2
                draw.text((x, y), line, font=self.font_medium, fill=(255, 255, 255))
                y += 50
            
            y += 20  # Space between elements
        
        # Add hashtags
        hashtags = " ".join([f"#{tag}" for tag in storytelling_dict["recommended_hashtags"]])
        hashtags_width = draw.textlength(hashtags, font=self.font_small)
        x = (width - hashtags_width) / 2
        draw.text((x, height + 260), hashtags, font=self.font_small, fill=(200, 200, 200))
        
        canvas.save(output_path)
        logger.info(f"✅ Story-focused social post saved to {output_path}")
        return output_path
    
    def create_ecommerce_content(self, storytelling_dict) -> dict:
        """Format content to emphasize the story and connection"""
        logger.info("🛒 Creating story-focused e-commerce content...")
        
        # Detect region for platform-specific formatting
        region = "India"
        if "Jaipur" in storytelling_dict["cultural_elements"]:
            region = "Rajasthan"
        elif "Kutch" in storytelling_dict["cultural_elements"]:
            region = "Gujarat"
        
        ecommerce_content = {
            "title": f"{storytelling_dict['story_title']} | Handcrafted by {region} Artisan",
            "description": (
                f"Experience the story behind this creation: {storytelling_dict['emotional_theme']}. "
                "This piece represents generations of tradition and cultural heritage. "
                "Each element carries deep meaning in Indian craftsmanship, connecting you to "
                "the artisan's journey and the cultural wisdom passed down through generations."
            ),
            "story_section": {
                "headline": storytelling_dict['story_title'],
                "narrative": "\n\n".join(storytelling_dict["image_prompts"]),
                "cultural_significance": (
                    "In {region} tradition, these elements represent {elements}. "
                    "This practice has been preserved through generations as a "
                    "sacred art form, embodying the Indian concept of 'shilp' - "
                    "where art and spirituality intertwine."
                ).format(
                    region=region,
                    elements=", ".join(storytelling_dict["cultural_elements"][:2])
                )
            },
            "product_representation": {
                "description": "This product is a physical representation of the story above",
                "meaning": (
                    "Rather than just a functional item, this creation embodies "
                    "cultural heritage and emotional meaning. The physical form "
                    "serves as a vessel for the story and tradition it represents."
                )
            },
            "tags": storytelling_dict["cultural_elements"] + ["Indian", "artisan", "handmade", "story", "cultural heritage", "traditional"] + storytelling_dict["recommended_hashtags"],
            "indian_platform_specifics": {
                "flipkart": {
                    "category": "Home & Kitchen > Decor > Handicrafts",
                    "attributes": {
                        "Craft Type": "Storytelling Art Piece",
                        "Region": region,
                        "Story Theme": storytelling_dict["emotional_theme"],
                        "Cultural Elements": ", ".join(storytelling_dict["cultural_elements"])
                    }
                },
                "meesho": {
                    "category": "Home Decor > Storytelling Art",
                    "attributes": {
                        "Story Title": storytelling_dict["story_title"],
                        "Emotional Theme": storytelling_dict["emotional_theme"],
                        "Cultural Elements": ", ".join(storytelling_dict["cultural_elements"])
                    }
                }
            }
        }
        
        logger.info("✅ Story-focused e-commerce content created")
        return ecommerce_content