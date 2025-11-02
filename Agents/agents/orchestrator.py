# agents/orchestrator.py
"""
🎼 The Orchestrator Agent (Complete Storytelling Pipeline)
- Coordinates all agents for Indian artisans
-                    results["outputs"]["enhanced_images"] = enhanced_images
                    print(f"🎯 Generated {len(enhanced_images)} enhanced product images")
                    
                except Exception as e:
                    print(f"⚠️ Image enhancement failed: {str(e)}")
                    logger.warning(f"Image enhancement failed: {str(e)}")
                    # Continue with storytelling even if enhancement fails
            elif photo_path and os.path.exists(photo_path) and not self.curator_available:
                print("\n⚠️ Step 0: Curator not available - skipping image enhancement")
                logger.warning("Photo provided but curator not available for enhancement")s the full creative storytelling workflow
- Handles error recovery and validation
- Outputs complete marketing kit with storytelling images
"""

import os
import json
import logging
from curator_agent import CuratorAgent
from storyteller_agent import StorytellerAgent
from image_generator_agent import ImageGeneratorAgent
from synthesizer_agent import ContentSynthesizer
from pricing_agent import DynamicPricingAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Orchestrator:
    """
    The Orchestrator Agent for Complete Storytelling
    Goal: Manage the full creative storytelling workflow for Indian artisans
    
    Process:
    1. Storyteller: Create storytelling image prompts
    2. Image Generator: Generate images from prompts
    3. Synthesizer: Create marketing assets from storytelling images
    """
    
    def __init__(self):
        # Skip curator for now to avoid initialization timeouts
        logger.info("⚠️ Curator Agent disabled to avoid initialization issues - Image enhancement will be skipped")
        self.curator = None
        self.curator_available = False
            
        try:
            self.storyteller = StorytellerAgent()
            logger.info("✅ Storyteller Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Storyteller initialization failed: {str(e)}")
            raise
            
        try:
            self.image_generator = ImageGeneratorAgent()
            logger.info("✅ Image Generator Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Image Generator initialization failed: {str(e)}")
            raise
            
        try:
            self.synthesizer = ContentSynthesizer()
            logger.info("✅ Synthesizer Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Synthesizer initialization failed: {str(e)}")
            raise
        
        try:
            self.pricing_agent = DynamicPricingAgent()
            logger.info("✅ Pricing Agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Pricing Agent initialization failed: {str(e)}")
            raise
    
    def get_model_status(self) -> dict:
        """Get status information about all models being used"""
        try:
            image_model_info = self.image_generator.get_current_model_info()
            return {
                "image_generator": image_model_info,
                "storyteller": "Gemini 2.0 Flash",
                "synthesizer": "PIL/Local Processing"
            }
        except Exception as e:
            logger.error(f"❌ Error getting model status: {str(e)}")
            return {"error": str(e)}
    
    def reset_image_model(self):
        """Reset image generator to primary model"""
        try:
            self.image_generator.reset_to_primary_model()
            logger.info("✅ Image generator reset to primary model")
            return True
        except Exception as e:
            logger.error(f"❌ Error resetting image model: {str(e)}")
            return False
    
    def run_storytelling_pipeline(self, artisan_description: str, output_dir: str = "storytelling_kit", photo_path: str = None) -> dict:
        """
        Run the complete storytelling pipeline with optional product image enhancement
        
        Args:
            artisan_description: Description of the artisan/product
            output_dir: Directory to save outputs
            photo_path: Optional path to product image for enhancement
            
        Returns paths to all generated assets including enhanced images
        """
        results = {
            "status": "processing",
            "artisan_description": artisan_description,
            "outputs": {}
        }
        
        try:
            # Step 0: Enhanced Product Images (if photo provided)
            if photo_path and os.path.exists(photo_path) and self.curator_available:
                print("\n🎨 Step 0: Enhancing product image...")
                try:
                    # Create enhanced versions using curator
                    enhanced_images = []
                    
                    # Studio shot enhancement
                    studio_shot = self.curator.create_studio_shot(photo_path, upscale=True)
                    studio_path = os.path.join(output_dir, "enhanced_studio_shot.jpg")
                    studio_shot.save(studio_path)
                    enhanced_images.append(studio_path)
                    print(f"✅ Studio shot saved to {studio_path}")
                    
                    # Lifestyle mockup enhancement  
                    lifestyle_shot = self.curator.create_lifestyle_mockup(photo_path, upscale=True)
                    lifestyle_path = os.path.join(output_dir, "enhanced_lifestyle.jpg")
                    lifestyle_shot.save(lifestyle_path)
                    enhanced_images.append(lifestyle_path)
                    print(f"✅ Lifestyle shot saved to {lifestyle_path}")
                    
                    # Custom enhancement with artisan description
                    custom_enhanced = self.curator.enhance(photo_path, f"Professional product photography of {artisan_description}", upscale=True)
                    custom_path = os.path.join(output_dir, "enhanced_custom.jpg")
                    custom_enhanced.save(custom_path)
                    enhanced_images.append(custom_path)
                    print(f"✅ Custom enhanced image saved to {custom_path}")
                    
                    results["outputs"]["enhanced_images"] = enhanced_images
                    print(f"� Generated {len(enhanced_images)} enhanced product images")
                    
                except Exception as e:
                    print(f"⚠️ Image enhancement failed: {str(e)}")
                    logger.warning(f"Image enhancement failed: {str(e)}")
                    # Continue with storytelling even if enhancement fails
            
            # 1. Storyteller: Create storytelling image prompts and story text
            print("\n📖 Step 1: Generating storytelling content...")
            image_prompts = self.storyteller.generate_image_prompts(artisan_description)
            validated_prompts = self.storyteller.validate_prompts(image_prompts, artisan_description)
            
            # Save storytelling data for next steps
            with open("image_prompts.json", "w", encoding="utf-8") as f:
                json.dump(validated_prompts, f, indent=2, ensure_ascii=False)
            results["outputs"]["storytelling"] = validated_prompts
            
            print(f"✅ Story Title: {validated_prompts['story_title']}")
            print(f"📖 Story Text: {validated_prompts.get('story_text', 'Not available')[:100]}...")
            print(f"✨ Emotional Theme: {validated_prompts['emotional_theme']}")
            print(f"🖼️ Image Prompts: {validated_prompts['prompt_count']}")
            
            # 2. Image Generator: Create storytelling images from prompts
            print("\n🖼️ Step 2: Generating storytelling images...")
            story_image_paths = self.image_generator.create_story_images(validated_prompts, output_dir="story_images")
            results["outputs"]["story_images"] = story_image_paths
            
            # 3. Synthesizer: Create marketing assets
            print("\n📱 Step 3: Creating marketing assets...")
            
            # Social post with storytelling image
            if story_image_paths:
                social_post = self.synthesizer.create_story_post(
                    validated_prompts, 
                    story_image_paths[0],  # Use first storytelling image
                    output_path=os.path.join(output_dir, "story_post.jpg")
                )
                results["outputs"]["social_post"] = social_post
                print(f"✅ Story-focused social post saved to {social_post}")
            
            # E-commerce content
            ecommerce = self.synthesizer.create_ecommerce_content(validated_prompts)
            results["outputs"]["ecommerce"] = ecommerce
            print("✅ Story-focused e-commerce content formatted")
            
            # 4. Pricing Agent: Calculate dynamic pricing
            print("\n💰 Step 4: Calculating AI-powered dynamic pricing...")
            try:
                pricing_result = self.pricing_agent.calculate_price(
                    artisan_description,
                    validated_prompts,
                    material_cost=100.0  # Default material cost, can be parameterized
                )
                results["outputs"]["pricing"] = pricing_result
                print(f"✅ Suggested Price: ₹{pricing_result['suggested_price']}")
                print(f"   Price Range: ₹{pricing_result['price_range']['min']} - ₹{pricing_result['price_range']['max']}")
                print(f"   Success Probability: {pricing_result['success_probability']}%")
            except Exception as e:
                print(f"⚠️ Pricing calculation failed: {str(e)}")
                logger.warning(f"Pricing calculation failed: {str(e)}")
                # Continue without pricing
            
            # Save final results
            results["status"] = "success"
            results["message"] = "Storytelling marketing kit generated successfully!"
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            logger.error(f"❌ Pipeline failed: {str(e)}")
        
        return results
    
    def generate_marketing_kit(self, artisan_description: str, output_dir: str = "storytelling_kit"):
        """Generate complete storytelling marketing kit in organized directory"""
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Run pipeline
        results = self.run_storytelling_pipeline(artisan_description, output_dir)
        
        if results["status"] == "success":
            # Save results
            kit = {
                "overview": {
                    "status": "success",
                    "description": "Complete storytelling marketing kit for Indian artisan",
                    "artisan_description": artisan_description,
                    "story_title": results["outputs"]["image_prompts"]["story_title"],
                    "emotional_theme": results["outputs"]["image_prompts"]["emotional_theme"],
                    "region": self._detect_region(artisan_description)
                },
                "assets": {
                    "story_images": [os.path.basename(p) for p in results["outputs"]["story_images"]],
                    "social_post": os.path.basename(results["outputs"]["social_post"])
                },
                "content": {
                    "storytelling": results["outputs"]["image_prompts"],
                    "ecommerce": results["outputs"]["ecommerce"]
                }
            }
            
            # Save to output directory
            with open(os.path.join(output_dir, "marketing_kit.json"), "w", encoding="utf-8") as f:
                json.dump(kit, f, indent=2, ensure_ascii=False)
            
            # Copy files to output directory
            for image_path in results["outputs"]["story_images"]:
                dst = os.path.join(output_dir, os.path.basename(image_path))
                if os.path.exists(image_path):
                    import shutil
                    shutil.copy2(image_path, dst)
            
            # Copy social post
            shutil.copy2(results["outputs"]["social_post"], 
                        os.path.join(output_dir, os.path.basename(results["outputs"]["social_post"])))
            
            print(f"\n🎉 COMPLETE STORYTELLING MARKETING KIT GENERATED IN: {os.path.abspath(output_dir)}")
            print(f"• Story Title: {kit['overview']['story_title']}")
            print(f"• Emotional Theme: {kit['overview']['emotional_theme']}")
            print(f"• Storytelling Images: {len(kit['assets']['story_images'])}")
            print(f"• Social Media Post: {kit['assets']['social_post']}")
            return True
        
        print("\n❌ FAILED TO GENERATE MARKETING KIT")
        return False
    
    def _detect_region(self, description: str) -> str:
        """Detect Indian region from description for marketing targeting"""
        description = description.lower()
        
        if "jaipur" in description or "rajasthan" in description:
            return "Rajasthan (Jaipur Blue Pottery)"
        elif "kutch" in description or "gujarat" in description:
            return "Gujarat (Kutch Pottery)"
        else:
            return "General Indian Artisan"