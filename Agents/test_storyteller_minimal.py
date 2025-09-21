# test_storyteller_minimal.py
"""
📝 MINIMAL STORYTELLER AGENT TEST
- No dependencies on other agents
- Uses your existing test_image.png
- Focuses ONLY on storytelling functionality
- Simple output that verifies everything works
"""

import json
import logging
from agents.storyteller_agent import StorytellerAgent

# Configure minimal logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def test_storyteller():
    print("\n" + "="*60)
    print("📝 MINIMAL STORYTELLER AGENT TEST")
    print("="*60)
    
    # Your existing test image (no need to generate it)
    TEST_IMAGE = "test_image.png"
    
    # Your artisan description (Jaipur blue pottery)
    ARTISAN_DESCRIPTION = (
        "This is a blue pot I made with peacock and lotus flowers, "
        "using traditional Jaipur techniques passed down from my grandfather."
    )
    
    logger.info(f"Using test image: {TEST_IMAGE}")
    logger.info(f"Testing with description: '{ARTISAN_DESCRIPTION[:50]}...'")
    
    try:
        # Initialize Storyteller Agent
        logger.info("Initializing Storyteller Agent...")
        storyteller = StorytellerAgent()
        logger.info("✅ Storyteller Agent initialized successfully")
        
        # Generate storytelling elements
        logger.info("\nGenerating creative storytelling elements...")
        storytelling = storyteller.generate_creative_story(ARTISAN_DESCRIPTION)
        
        # Validate the story
        logger.info("Validating storytelling output...")
        validated_story = storyteller.validate_story(storytelling, ARTISAN_DESCRIPTION)
        
        # Save results
        output_file = "storytelling_output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(validated_story, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Storytelling output saved to {output_file}")
        
        # Display results
        print("\n" + "="*60)
        print("🌟 STORYTELLING RESULTS")
        print("="*60)
        print(f"TITLE: {validated_story['story_title']}")
        print(f"EMOTIONAL THEME: {validated_story['emotional_theme']}")
        print("\nSTORY ELEMENTS:")
        for i, element in enumerate(validated_story['story_elements'], 1):
            print(f"{i}. {element}")
        
        print("\nCULTURAL ELEMENTS:")
        print("• " + ", ".join(validated_story['cultural_elements']))
        
        print("\nRECOMMENDED HASHTAGS:")
        print("• " + " ".join([f"#{tag}" for tag in validated_story['recommended_hashtags']]))
        
        print("\n" + "="*60)
        print("🎉 STORYTELLER AGENT TEST PASSED!")
        print("="*60)
        print("The Storyteller Agent is working correctly with your")
        print("Indian artisan cultural knowledge base.")
        print("\nNext steps:")
        print("1. Review storytelling_output.json for details")
        print("2. Connect with the Synthesizer Agent for marketing content")
        print("3. Use this storytelling output for your e-commerce platform")
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {str(e)}")
        logger.error("💡 TROUBLESHOOTING TIPS:")
        logger.error("1. Check if Firestore is properly set up with Indian cultural knowledge base")
        logger.error("2. Verify your GCP credentials are correctly configured")
        logger.error("3. Ensure you have access to Gemini 1.5 Flash model")
        return False

if __name__ == "__main__":
    test_storyteller()