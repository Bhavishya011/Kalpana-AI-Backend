"""
🖼️ Image Generator Agent
- Generates images from storytelling prompts
- Uses Imagen for high-quality image generation
- Creates culturally authentic visuals for Indian artisans
"""

import io
import os
import logging
from PIL import Image
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageGeneratorAgent:
    """
    Image Generator Agent
    Uses Imagen to create images from storytelling prompts with fallback model support
    """
    
    def __init__(self):
        try:
            # Initialize Vertex AI
            vertexai.init(project="nodal-fountain-470717-j1", location="us-central1")
            
            # Primary model - high quality but has quota limits
            self.primary_model_name = "imagen-4.0-generate-001"
            self.primary_model = ImageGenerationModel.from_pretrained(self.primary_model_name)
            
            # Fallback model - faster generation with higher quota
            self.fallback_model_name = "imagegeneration@006"
            self.fallback_model = ImageGenerationModel.from_pretrained(self.fallback_model_name)
            
            # Track which model to use (starts with primary)
            self.use_fallback = False
            
            logger.info("✅ Imagen models loaded successfully (primary + fallback)")
        except Exception as e:
            logger.error(f"❌ Image generation initialization failed: {str(e)}")
            raise
    
    def generate_story_image(self, prompt: str, output_path: str = "story_image.jpg") -> str:
        """Generate an image from a storytelling prompt with fallback model support"""
        logger.info(f"🖼️ Generating image for prompt: {prompt[:100]}...")
        
        # Determine which model to use
        current_model = self.fallback_model if self.use_fallback else self.primary_model
        model_name = self.fallback_model_name if self.use_fallback else self.primary_model_name
        
        try:
            # Generate image WITHOUT seed parameter to avoid watermark conflict
            images = current_model.generate_images(
                prompt=prompt,
                number_of_images=1,
                add_watermark=False  # Disable watermark to avoid conflicts
            )
            
            # Save the generated image
            images[0].save(location=output_path, include_generation_parameters=False)
            
            logger.info(f"✅ Story image saved to {output_path} (using {model_name})")
            return output_path
            
        except Exception as e:
            error_str = str(e)
            logger.error(f"❌ Error generating story image with {model_name}: {error_str}")
            
            # Check if it's a quota error and we haven't switched to fallback yet
            if "429" in error_str or "Quota exceeded" in error_str:
                if not self.use_fallback:
                    logger.info("🔄 Quota exceeded on primary model, switching to fallback model...")
                    self.use_fallback = True
                    # Retry with fallback model
                    return self.generate_story_image(prompt, output_path)
                else:
                    logger.error("❌ Quota exceeded on both models!")
                    raise Exception("Both primary and fallback models have exceeded quotas")
            
            # If not a quota error, try basic retry without special parameters
            try:
                logger.info(f"🔄 Retrying image generation with minimal parameters on {model_name}...")
                images = current_model.generate_images(
                    prompt=prompt,
                    number_of_images=1
                )
                
                images[0].save(location=output_path, include_generation_parameters=False)
                logger.info(f"✅ Story image saved to {output_path} (retry successful with {model_name})")
                return output_path
                
            except Exception as retry_error:
                retry_error_str = str(retry_error)
                logger.error(f"❌ Retry also failed on {model_name}: {retry_error_str}")
                
                # If retry also has quota error and we're on primary model, try fallback
                if ("429" in retry_error_str or "Quota exceeded" in retry_error_str) and not self.use_fallback:
                    logger.info("🔄 Quota exceeded on retry, switching to fallback model...")
                    self.use_fallback = True
                    return self.generate_story_image(prompt, output_path)
                
                raise
    
    def reset_to_primary_model(self):
        """Reset to use primary model (can be called if quotas reset)"""
        self.use_fallback = False
        logger.info("🔄 Reset to primary model")
    
    def get_current_model_info(self):
        """Get information about which model is currently being used"""
        current_model_name = self.fallback_model_name if self.use_fallback else self.primary_model_name
        return {
            "current_model": current_model_name,
            "using_fallback": self.use_fallback,
            "primary_model": self.primary_model_name,
            "fallback_model": self.fallback_model_name
        }
    
    def create_story_images(self, image_prompts_dict, output_dir: str = "story_images") -> list:
        """Create all story images from prompts"""
        logger.info("🎨 Creating story images from prompts...")
        model_info = self.get_current_model_info()
        logger.info(f"📊 Starting with model: {model_info['current_model']}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        image_paths = []
        
        # Generate each image
        for i, prompt in enumerate(image_prompts_dict["image_prompts"]):
            output_path = os.path.join(output_dir, f"story_image_{i+1}.jpg")
            logger.info(f"  → Generating image {i+1}/{len(image_prompts_dict['image_prompts'])}")
            
            try:
                image_path = self.generate_story_image(prompt, output_path)
                image_paths.append(image_path)
            except Exception as e:
                logger.error(f"  ❌ Failed to generate image {i+1}: {str(e)}")
        
        # Final model status
        final_model_info = self.get_current_model_info()
        if final_model_info['using_fallback']:
            logger.info(f"📊 Completed using fallback model: {final_model_info['current_model']}")
        
        logger.info(f"✅ Generated {len(image_paths)}/{len(image_prompts_dict['image_prompts'])} story images")
        return image_paths