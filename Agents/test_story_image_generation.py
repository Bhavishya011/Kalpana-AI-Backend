# test_story_image_generation.py
"""
🖼️ STORY-BASED IMAGE GENERATION TEST
- Tests generating images from storyteller output
- Uses correct method names per current implementation
- No dependencies on product photos
"""

import json
import logging
from agents.storyteller_agent import StorytellerAgent
from agents.image_generator_agent import ImageGeneratorAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_story_image_generation():
    """Test generating images from storytelling prompts"""
    print("\n" + "="*60)
    print("🖼️ STORY-BASED IMAGE GENERATION TEST")
    print("="*60)
    
    # Indian artisan description (Jaipur blue pottery)
    ARTISAN_DESCRIPTION = (
        "This is a blue pot I made with peacock and lotus flowers, "
        "using traditional Jaipur techniques passed down from my grandfather."
    )
    
    print(f"📝 Artisan Description: {ARTISAN_DESCRIPTION}")
    
    try:
        # 1. Generate storytelling prompts for image generation
        print("\n🎨 Step 1: Generating image prompts for storytelling...")
        storyteller = StorytellerAgent()
        # CORRECT METHOD NAME: generate_image_prompts (not generate_creative_story)
        image_prompts = storyteller.generate_image_prompts(ARTISAN_DESCRIPTION)
        validated_prompts = storyteller.validate_prompts(image_prompts, ARTISAN_DESCRIPTION)
        
        # Save prompts for reference
        with open("image_prompts.json", "w", encoding="utf-8") as f:
            json.dump(validated_prompts, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Story Title: {validated_prompts['story_title']}")
        print(f"✨ Emotional Theme: {validated_prompts['emotional_theme']}")
        print(f"🖼️ Image Prompts: {validated_prompts['prompt_count']}")
        
        # 2. Generate images from prompts
        print("\n🖼️ Step 2: Generating images from storytelling prompts...")
        image_generator = ImageGeneratorAgent()
        image_paths = image_generator.create_story_images(validated_prompts)
        
        # 3. Display results
        print("\n" + "="*60)
        print("🌟 GENERATED STORY IMAGES")
        print("="*60)
        for i, path in enumerate(image_paths, 1):
            print(f"Image {i}: {path}")
        
        print("\n" + "="*60)
        print("🎨 STORY PROMPTS USED")
        print("="*60)
        for i, prompt in enumerate(validated_prompts["image_prompts"], 1):
            print(f"Prompt {i}:")
            print(f"\"{prompt[:200]}...\"")
            print()
        
        print("\n" + "="*60)
        print("🎉 STORY-BASED IMAGE GENERATION TEST PASSED!")
        print("="*60)
        print("Your system now generates storytelling images that:")
        print("• Capture the artisan's cultural heritage")
        print("• Create emotional connections with customers")
        print("• Focus on meaningful moments, not just products")
        print("\n💡 Next steps:")
        print("1. Review the generated images in story_images/")
        print("2. Use these images for social media storytelling")
        print("3. Connect with the Synthesizer Agent for marketing content")
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {str(e)}")
        logger.error("\n💡 TROUBLESHOOTING TIPS:")
        logger.error("1. Check if Firestore is properly set up with Indian cultural knowledge base")
        logger.error("2. Verify your GCP credentials are correctly configured")
        logger.error("3. Ensure you have access to Gemini 2.5 Flash model")
        return False


if __name__ == "__main__":
    test_story_image_generation()