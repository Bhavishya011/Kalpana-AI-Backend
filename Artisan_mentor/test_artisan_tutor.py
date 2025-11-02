"""
Simple test to verify Artisan Mentor functionality without ADK dependency.
This directly tests the core HybridArtisanTutor class.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Test the core tutor functionality (bypassing ADK)
try:
    from artisan_mentor.tools import (
        start_artisan_journey,
        get_adaptive_lesson,
        analyze_craft_for_learning
    )
    
    print("✅ Successfully imported artisan_mentor tools")
    
    # Test 1: Start artisan journey
    print("\n--- Test 1: Starting Artisan Journey ---")
    test_profile = {
        "user_id": "test_user_123",
        "name": "Rajesh Kumar",
        "learning_style": "visual",
        "language": "en",
        "current_skill_level": "beginner",
        "craft_analysis": {
            "craft_name": "Pottery",
            "region": "Jaipur",
            "materials": ["clay", "glaze"],
            "skill_level_required": "Beginner"
        }
    }
    
    result = start_artisan_journey(test_profile)
    print(f"Status: {result.get('status')}")
    print(f"User ID: {result.get('user_id')}")
    print(f"Starting Module: {result.get('starting_point', {}).get('module')}")
    print(f"Starting Lesson: {result.get('starting_point', {}).get('lesson')}")
    
    if result.get('status') == 'success':
        print("✅ Test 1 PASSED: Journey started successfully")
    else:
        print("❌ Test 1 FAILED:", result.get('message'))
    
    # Test 2: Get adaptive lesson
    print("\n--- Test 2: Getting First Lesson ---")
    if result.get('status') == 'success':
        user_id = result['user_id']
        lesson_id = result['starting_point']['lesson']
        
        lesson_result = get_adaptive_lesson(user_id, lesson_id, "multimodal")
        print(f"Status: {lesson_result.get('status')}")
        if lesson_result.get('status') == 'success':
            lesson = lesson_result.get('lesson', {})
            print(f"Lesson Title: {lesson.get('title')}")
            print(f"Lesson Objective: {lesson.get('objective')}")
            print("✅ Test 2 PASSED: Lesson retrieved successfully")
        else:
            print("❌ Test 2 FAILED:", lesson_result.get('message'))
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60)
    print("\nNote: Full functionality requires:")
    print("  - Google Cloud credentials configured")
    print("  - Firestore database setup")
    print("  - Cloud Storage bucket created")
    print("  - Vertex AI API enabled")
    
except Exception as e:
    print(f"❌ TEST FAILED: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
