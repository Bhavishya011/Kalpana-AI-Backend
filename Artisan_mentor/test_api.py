"""
Comprehensive test suite for Artisan Mentor API
Tests all core functionality without requiring full Google Cloud setup
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Module Imports")
    print("="*60)
    
    try:
        from artisan_mentor.tools import (
            start_artisan_journey,
            get_adaptive_lesson,
            submit_adaptive_work,
            get_comprehensive_dashboard,
            analyze_craft_for_learning,
            text_to_speech_assist,
            speech_to_text_assist
        )
        print("✅ Successfully imported all tools")
        
        from artisan_mentor.agent import agent
        print(f"✅ Agent loaded: {agent.name}")
        print(f"✅ Available tools: {', '.join(agent.list_tools())}")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_structure():
    """Test agent structure"""
    print("\n" + "="*60)
    print("TEST 2: Agent Structure")
    print("="*60)
    
    try:
        from artisan_mentor.agent import agent
        
        assert agent.name == "ultimate-artisan-tutor"
        print(f"✅ Agent name: {agent.name}")
        
        assert len(agent.list_tools()) == 7
        print(f"✅ Tool count: {len(agent.list_tools())}")
        
        # Test getting a tool
        tool = agent.get_tool("start_artisan_journey")
        assert tool is not None
        print(f"✅ Tool retrieval works")
        
        return True
    except Exception as e:
        print(f"❌ Agent structure test failed: {str(e)}")
        return False

def test_start_journey():
    """Test starting a learning journey"""
    print("\n" + "="*60)
    print("TEST 3: Start Learning Journey")
    print("="*60)
    
    try:
        from artisan_mentor.tools import start_artisan_journey
        
        test_profile = {
            "user_id": "test_user_001",
            "name": "Priya Sharma",
            "learning_style": "visual",
            "language": "en",
            "current_skill_level": "beginner",
            "craft_analysis": {
                "craft_name": "Madhubani Painting",
                "region": "Bihar",
                "materials": ["natural dyes", "paper"],
                "skill_level_required": "Beginner"
            }
        }
        
        print("📤 Sending profile:", test_profile["name"])
        result = start_artisan_journey(test_profile)
        
        assert result.get("status") == "success", f"Expected success, got {result.get('status')}"
        assert "user_id" in result
        assert "starting_point" in result
        
        print(f"✅ Journey started successfully")
        print(f"   User ID: {result['user_id']}")
        print(f"   Starting Module: {result['starting_point'].get('module')}")
        print(f"   Starting Lesson: {result['starting_point'].get('lesson')}")
        print(f"   Welcome: {result.get('welcome_message', '')[:100]}...")
        
        return True, result
    except Exception as e:
        print(f"❌ Start journey test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def test_api_wrapper():
    """Test that API wrapper can be imported"""
    print("\n" + "="*60)
    print("TEST 4: API Wrapper")
    print("="*60)
    
    try:
        import api_main
        print(f"✅ API wrapper imported successfully")
        print(f"✅ FastAPI app: {api_main.app.title}")
        print(f"✅ Version: {api_main.app.version}")
        
        # Check endpoints
        routes = [route.path for route in api_main.app.routes]
        expected_endpoints = [
            "/", "/health", "/start-journey", "/get-lesson", 
            "/submit-work", "/dashboard", "/analyze-craft", "/tts", "/stt"
        ]
        
        for endpoint in expected_endpoints:
            if endpoint in routes:
                print(f"✅ Endpoint exists: {endpoint}")
            else:
                print(f"⚠️ Endpoint missing: {endpoint}")
        
        return True
    except Exception as e:
        print(f"❌ API wrapper test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_curriculum_structure():
    """Test curriculum data structure"""
    print("\n" + "="*60)
    print("TEST 5: Curriculum Structure")
    print("="*60)
    
    try:
        from artisan_mentor.tutor import PROGRESSIVE_CURRICULUM
        
        if not PROGRESSIVE_CURRICULUM:
            print("⚠️ Curriculum is empty - check data/curriculum.json")
            return False
        
        print(f"✅ Curriculum loaded with {len(PROGRESSIVE_CURRICULUM)} modules")
        
        for module_key, module_data in PROGRESSIVE_CURRICULUM.items():
            title = module_data.get("title", "Untitled")
            lessons = module_data.get("lessons", [])
            print(f"   📚 {title}: {len(lessons)} lessons")
        
        return True
    except Exception as e:
        print(f"❌ Curriculum test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪"*30)
    print("ARTISAN MENTOR API TEST SUITE")
    print("🧪"*30)
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: Agent Structure
    results.append(("Agent Structure", test_agent_structure()))
    
    # Test 3: Start Journey (will fail without Firestore but tests logic)
    journey_result = test_start_journey()
    results.append(("Start Journey", journey_result[0]))
    
    # Test 4: API Wrapper
    results.append(("API Wrapper", test_api_wrapper()))
    
    # Test 5: Curriculum
    results.append(("Curriculum", test_curriculum_structure()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n📝 Notes:")
        print("  - Full functionality requires Google Cloud credentials")
        print("  - Firestore database must be configured")
        print("  - Cloud Storage bucket must exist")
        print("  - Run './deploy.ps1' to deploy to Cloud Run")
    else:
        print("\n⚠️ Some tests failed - review errors above")
    
    print("\n" + "="*60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
