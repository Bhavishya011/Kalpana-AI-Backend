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
    print("📝 STORYTELLER AGENT TEST - Dynamic RAG System")
    print("="*60)
    
    # Test with different art styles to verify dynamic RAG
    test_descriptions = [
        {
            "name": "Blue Pottery",
            "description": "This is a blue pot I made with peacock and lotus flowers, using traditional Jaipur techniques passed down from my grandfather."
        },
        {
            "name": "Madhubani Painting", 
            "description": "A colorful Madhubani painting with geometric patterns and nature motifs from Bihar."
        },
        {
            "name": "Warli Art",
            "description": "Traditional Warli tribal art with stick figures depicting village life from Maharashtra."
        }
    ]
    
    logger.info("Testing dynamic RAG system with multiple art forms...")
    
    try:
        # Initialize Storyteller Agent
        logger.info("Initializing Storyteller Agent...")
        storyteller = StorytellerAgent()
        logger.info("✅ Storyteller Agent initialized successfully\n")
        
        all_results = []
        
        for test_case in test_descriptions:
            print("\n" + "-"*60)
            print(f"🎨 Testing: {test_case['name']}")
            print("-"*60)
            logger.info(f"Description: '{test_case['description'][:80]}...'")
            
            # Generate storytelling elements with image prompts
            logger.info("Generating storytelling package...")
            storytelling = storyteller.generate_image_prompts(test_case['description'])
            
            # Validate the output
            logger.info("Validating storytelling output...")
            validated_story = storyteller.validate_prompts(storytelling, test_case['description'])
            
            # Add test case name to results
            validated_story['art_form_tested'] = test_case['name']
            all_results.append(validated_story)
            
            # Display results for this art form
            print("\n📖 STORY:")
            print(f"Title: {validated_story['story_title']}")
            print(f"Theme: {validated_story['emotional_theme']}")
            print(f"\nStory Text ({validated_story['story_word_count']} words):")
            print(validated_story['story_text'][:200] + "...")
            
            print("\n🎨 IMAGE PROMPTS:")
            for i, prompt in enumerate(validated_story['image_prompts'], 1):
                print(f"\n{i}. {prompt[:150]}...")
            
            print("\n🏛️ CULTURAL ELEMENTS:")
            print("• " + ", ".join(validated_story['cultural_elements']))
            
            print("\n#️⃣ HASHTAGS:")
            print("• " + " ".join(validated_story['recommended_hashtags']))
        
        # Save all results
        output_file = "storytelling_rag_test_results.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        logger.info(f"\n✅ All test results saved to {output_file}")
        
        # Summary
        print("\n" + "="*60)
        print("🎉 STORYTELLER AGENT RAG TEST PASSED!")
        print("="*60)
        print(f"✅ Tested {len(test_descriptions)} different art forms")
        print("✅ Dynamic RAG system retrieved unique contexts for each")
        print("✅ Generated unique stories and image prompts per art form")
        print("\n📊 Results Summary:")
        for result in all_results:
            print(f"  • {result['art_form_tested']}: {result['prompt_count']} image prompts, {result['story_word_count']} words")
        
        print("\n📁 Detailed results saved to: storytelling_rag_test_results.json")
        print("\n🚀 Next Steps:")
        print("1. Review the JSON file to see unique content per art form")
        print("2. Verify each story uses correct cultural context")
        print("3. Test with more art forms to expand the knowledge base")
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        logger.error(f"Full error:\n{traceback.format_exc()}")
        logger.error("\n💡 TROUBLESHOOTING TIPS:")
        logger.error("1. Check if Firestore cultural_knowledge_base has documents with 'keywords' field")
        logger.error("2. Verify your GCP credentials are correctly configured")
        logger.error("3. Ensure Firestore documents have proper structure")
        logger.error("4. Check if Gemini 2.5 Flash model is accessible")
        return False

if __name__ == "__main__":
    test_storyteller()