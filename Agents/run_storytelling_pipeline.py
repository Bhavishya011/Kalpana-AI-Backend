# run_storytelling_pipeline.py
"""
🚀 COMPLETE STORYTELLING PIPELINE EXECUTION
- Runs the full Orchestrator workflow
- Creates storytelling images and marketing content
- Organizes everything into a marketing kit
"""

import logging
from agents.orchestrator import Orchestrator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    print("\n" + "="*60)
    print("🚀 COMPLETE STORYTELLING PIPELINE EXECUTION")
    print("="*60)
    
    # Configuration for Indian artisan
    ARTISAN_DESCRIPTION = (
        "This is a blue pot I made with peacock and lotus flowers, "
        "using traditional Jaipur techniques passed down from my grandfather."
    )
    
    print(f"📝 Artisan Description: {ARTISAN_DESCRIPTION}")
    print(f"💡 Tip: Edit this description for different artisans")
    
    try:
        # Initialize Orchestrator
        print("\n🔧 Initializing Orchestrator...")
        orchestrator = Orchestrator()
        
        # Run the complete storytelling pipeline
        print("\n🚀 STARTING COMPLETE STORYTELLING PIPELINE...")
        success = orchestrator.generate_marketing_kit(
            artisan_description=ARTISAN_DESCRIPTION,
            output_dir="storytelling_kit"
        )
        
        if success:
            print("\n" + "="*60)
            print("🎉 COMPLETE STORYTELLING PIPELINE SUCCESS!")
            print("="*60)
            print("Your system has generated a complete marketing kit with:")
            print("• Storytelling images capturing the artisan's journey")
            print("• Social media content focused on cultural heritage")
            print("• E-commerce content emphasizing emotional connection")
            print("\n📁 Where to find your content:")
            print("1. storytelling_kit/ - Complete marketing kit")
            print("2. storytelling_kit/story_images/ - Storytelling images")
            print("3. storytelling_kit/marketing_kit.json - Metadata")
            print("\n💡 Next steps:")
            print("1. Review the storytelling_kit directory")
            print("2. Share the story post on social media")
            print("3. Add the e-commerce content to your product listing")
            return True
        else:
            return False
            
    except Exception as e:
        logger.error(f"\n❌ PIPELINE FAILED: {str(e)}")
        logger.error("\n💡 TROUBLESHOOTING TIPS:")
        logger.error("1. Check if Firestore is properly set up with Indian cultural knowledge base")
        logger.error("2. Verify your GCP credentials are correctly configured")
        logger.error("3. Ensure you have access to Gemini 1.5 Flash model")
        logger.error("4. Check if Imagen model is properly configured")
        return False


if __name__ == "__main__":
    main()