"""
Test script for KalpanaAI Support Chatbot API
"""

import requests
import json

# API URL - Update this after deployment
API_URL = "http://localhost:8083"  # Local
# API_URL = "https://support-chatbot-api-XXXXX.run.app"  # Production

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing /health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_chat_english():
    """Test chat in English"""
    print("\n💬 Testing chat in English...")
    payload = {
        "message": "How do I create my first product?",
        "language": "en-US"
    }
    response = requests.post(f"{API_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Bot: {data['response'][:200]}...")

def test_chat_hindi():
    """Test chat in Hindi"""
    print("\n🇮🇳 Testing chat in Hindi...")
    payload = {
        "message": "मुझे Market Pulse के बारे में बताएं",
        "language": "hi-IN"
    }
    response = requests.post(f"{API_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Bot: {data['response'][:200]}...")

def test_chat_with_history():
    """Test chat with conversation history"""
    print("\n📜 Testing chat with history...")
    
    # First message
    session_id = "test_session_123"
    
    payload1 = {
        "message": "What is Artisan Mentor?",
        "session_id": session_id,
        "language": "en-US"
    }
    response1 = requests.post(f"{API_URL}/chat", json=payload1)
    data1 = response1.json()
    print(f"User: What is Artisan Mentor?")
    print(f"Bot: {data1['response'][:150]}...")
    
    # Follow-up message with history
    payload2 = {
        "message": "How do I earn points?",
        "session_id": session_id,
        "language": "en-US",
        "history": [
            {"role": "user", "content": "What is Artisan Mentor?"},
            {"role": "bot", "content": data1['response']}
        ]
    }
    response2 = requests.post(f"{API_URL}/chat", json=payload2)
    data2 = response2.json()
    print(f"\nUser: How do I earn points?")
    print(f"Bot: {data2['response'][:150]}...")

def test_quick_help():
    """Test quick help endpoint"""
    print("\n⚡ Testing /quick-help endpoint...")
    
    categories = ["product-creation", "artisan-mentor", "pricing"]
    
    for category in categories:
        response = requests.post(f"{API_URL}/quick-help?category={category}")
        data = response.json()
        print(f"\n{category}:")
        print(f"{data['response'][:100]}...")

def test_multilingual():
    """Test multiple Indian languages"""
    print("\n🌍 Testing multilingual support...")
    
    test_cases = [
        ("How much does it cost?", "en-US", "English"),
        ("यह कितने का है?", "hi-IN", "Hindi"),
        ("দাম কত?", "bn-IN", "Bengali"),
        ("விலை என்ன?", "ta-IN", "Tamil"),
    ]
    
    for message, lang, name in test_cases:
        print(f"\n{name} ({lang}):")
        print(f"User: {message}")
        payload = {"message": message, "language": lang}
        response = requests.post(f"{API_URL}/chat", json=payload)
        data = response.json()
        print(f"Bot: {data['response'][:100]}...")

def test_feature_questions():
    """Test questions about specific features"""
    print("\n🎯 Testing feature-specific questions...")
    
    questions = [
        "What is The Muse?",
        "How does Market Pulse work?",
        "What languages do you support?",
        "Tell me about pricing recommendations",
        "How do I prepare for Diwali sales?",
        "What crafts are popular in South India?"
    ]
    
    for question in questions:
        print(f"\n❓ {question}")
        payload = {"message": question, "language": "en-US"}
        response = requests.post(f"{API_URL}/chat", json=payload)
        data = response.json()
        print(f"💡 {data['response'][:120]}...")

if __name__ == "__main__":
    print("🚀 Starting KalpanaAI Support Chatbot API Tests")
    print(f"📍 API URL: {API_URL}")
    
    try:
        # Run all tests
        test_health()
        test_chat_english()
        test_chat_hindi()
        test_chat_with_history()
        test_quick_help()
        test_multilingual()
        test_feature_questions()
        
        print("\n\n✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to {API_URL}")
        print("Make sure the API server is running:")
        print("  python main.py")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
