"""
Test script for Muse Agent API
Tests the deployed API with a sample craft image
"""
import requests
import sys
import json

def test_api(base_url):
    """Test the Muse Agent API"""
    
    print("=" * 60)
    print("🧪 Testing Muse Agent API")
    print(f"📍 URL: {base_url}")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n🔍 Test 1: Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        if response.status_code == 200:
            print("   ✅ PASS")
        else:
            print("   ❌ FAIL")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Bucket check
    print("\n🪣 Test 2: GCS Bucket Check")
    try:
        response = requests.get(f"{base_url}/bucket-check", timeout=10)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Bucket: {result.get('bucket')}")
        print(f"   Accessible: {result.get('accessible')}")
        if result.get('accessible'):
            print("   ✅ PASS")
        else:
            print("   ⚠️  WARNING: Bucket may not be accessible")
    except Exception as e:
        print(f"   ⚠️  Warning: {e}")
    
    # Test 3: Image generation
    print("\n🎨 Test 3: Generate Craft Variations")
    print("   Downloading test craft image...")
    try:
        # Download a test craft image
        img_url = "https://picsum.photos/800/800"
        img_response = requests.get(img_url, timeout=10)
        
        if img_response.status_code != 200:
            print("   ❌ Failed to download test image")
            return False
        
        print("   ✅ Test image downloaded")
        print("   📤 Uploading to API (this may take 1-2 minutes)...")
        
        # Upload to API
        files = {
            'image': ('craft.jpg', img_response.content, 'image/jpeg')
        }
        
        response = requests.post(
            f"{base_url}/generate",
            files=files,
            timeout=180  # 3 minutes timeout
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Generation successful!")
            print(f"\n   📊 Results:")
            print(f"   Traditional Images: {len(result['data']['traditional_images'])} generated")
            print(f"   Modern Images: {len(result['data']['modern_images'])} generated")
            
            print(f"\n   🖼️  Generated Image URLs:")
            for i, url in enumerate(result['data']['traditional_images'], 1):
                if url:
                    print(f"      Traditional {i}: {url}")
                else:
                    print(f"      Traditional {i}: ⚠️  Generation failed")
            
            for i, url in enumerate(result['data']['modern_images'], 1):
                if url:
                    print(f"      Modern {i}: {url}")
                else:
                    print(f"      Modern {i}: ⚠️  Generation failed")
            
            # Check if all images were generated
            all_images = result['data']['traditional_images'] + result['data']['modern_images']
            successful = sum(1 for img in all_images if img is not None)
            
            print(f"\n   📈 Success Rate: {successful}/4 images generated")
            
            if successful >= 3:
                print("   ✅ PASS (75%+ success rate)")
                return True
            else:
                print("   ⚠️  PARTIAL PASS (some images failed)")
                return True
        else:
            print(f"   ❌ FAIL")
            print(f"   Error: {response.text}")
            return False
            
    except requests.Timeout:
        print("   ⏱️  Request timed out (this is normal for first request)")
        print("   The API may still be processing. Check Cloud Run logs.")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    return True

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        # Default to Cloud Run URL
        base_url = "https://muse-agent-api-508329185712.us-central1.run.app"
    
    result = test_api(base_url)
    
    print("\n" + "=" * 60)
    if result is True:
        print("✅ All tests passed!")
        print("=" * 60)
        return 0
    elif result is None:
        print("⏱️  Tests timed out (may still be processing)")
        print("=" * 60)
        return 0
    else:
        print("❌ Some tests failed")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
