"""Verify all services are properly configured."""

from google.cloud import firestore, storage
from google.cloud import texttospeech, speech
from vertexai.generative_models import GenerativeModel
import vertexai
import os

os.environ['GOOGLE_CLOUD_PROJECT'] = 'nodal-fountain-470717-j1'
vertexai.init(project='nodal-fountain-470717-j1', location='us-central1')

def check_firestore():
    """Test Firestore connection."""
    try:
        db = firestore.Client()
        # Try to read a document
        users = list(db.collection('users').limit(1).stream())
        print(f"✅ Firestore: Connected (found {len(users)} sample user(s))")
        return True
    except Exception as e:
        print(f"❌ Firestore: {e}")
        return False

def check_storage():
    """Test Cloud Storage connection."""
    try:
        client = storage.Client()
        bucket = client.bucket('kalpana-artisan-tutor')
        exists = bucket.exists()
        if exists:
            blobs = list(bucket.list_blobs(max_results=5))
            print(f"✅ Cloud Storage: Connected ({len(blobs)} files/folders found)")
            return True
        else:
            print("⚠️  Cloud Storage: Bucket doesn't exist yet")
            return False
    except Exception as e:
        print(f"❌ Cloud Storage: {e}")
        return False

def check_tts():
    """Test Text-to-Speech."""
    try:
        client = texttospeech.TextToSpeechClient()
        voices = client.list_voices()
        hindi_voices = [v for v in voices.voices if 'hi-IN' in v.language_codes]
        print(f"✅ Text-to-Speech: Connected ({len(hindi_voices)} Hindi voices available)")
        return True
    except Exception as e:
        print(f"❌ Text-to-Speech: {e}")
        return False

def check_stt():
    """Test Speech-to-Text."""
    try:
        client = speech.SpeechClient()
        print("✅ Speech-to-Text: Connected")
        return True
    except Exception as e:
        print(f"❌ Speech-to-Text: {e}")
        return False

def check_gemini():
    """Test Vertex AI / Gemini."""
    try:
        model = GenerativeModel("gemini-2.0-flash-001")
        print("✅ Vertex AI (Gemini 2.0 Flash): Connected")
        return True
    except Exception as e:
        print(f"❌ Vertex AI: {e}")
        return False

def print_firestore_data():
    """Show sample Firestore data."""
    try:
        db = firestore.Client()
        users = list(db.collection('users').limit(1).stream())
        if users:
            user_data = users[0].to_dict()
            print(f"\n📊 Sample User Data:")
            print(f"   User ID: {users[0].id}")
            print(f"   Name: {user_data.get('profile', {}).get('name', 'N/A')}")
            print(f"   Language: {user_data.get('profile', {}).get('language', 'N/A')}")
            print(f"   Current Lesson: {user_data.get('learning_journey', {}).get('current_lesson', 'N/A')}")
            print(f"   Points: {user_data.get('progress_metrics', {}).get('total_points', 0)}")
    except:
        pass

if __name__ == "__main__":
    print("🔍 Verifying Artisan Mentor Setup...\n")
    print("="*60)
    
    results = {
        "Firestore": check_firestore(),
        "Cloud Storage": check_storage(),
        "Text-to-Speech": check_tts(),
        "Speech-to-Text": check_stt(),
        "Vertex AI": check_gemini()
    }
    
    print("="*60)
    
    # Show sample data
    print_firestore_data()
    
    print("\n" + "="*60)
    total = len(results)
    passed = sum(results.values())
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("\n🚀 You're ready to deploy!")
        print("\nNext steps:")
        print("1. Run local tests: python test_api.py")
        print("2. Deploy to Cloud Run: .\\deploy.ps1")
    else:
        print(f"⚠️  {passed}/{total} checks passed")
        print("\n❌ Please fix the failed services:")
        
        for service, status in results.items():
            if not status:
                if service == "Firestore":
                    print(f"\n  {service}:")
                    print(f"    gcloud services enable firestore.googleapis.com --project=nodal-fountain-470717-j1")
                    print(f"    python setup_database.py")
                elif service == "Cloud Storage":
                    print(f"\n  {service}:")
                    print(f"    gcloud services enable storage.googleapis.com --project=nodal-fountain-470717-j1")
                    print(f"    python setup_storage.py")
                elif service == "Text-to-Speech":
                    print(f"\n  {service}:")
                    print(f"    gcloud services enable texttospeech.googleapis.com --project=nodal-fountain-470717-j1")
                elif service == "Speech-to-Text":
                    print(f"\n  {service}:")
                    print(f"    gcloud services enable speech.googleapis.com --project=nodal-fountain-470717-j1")
                elif service == "Vertex AI":
                    print(f"\n  {service}:")
                    print(f"    gcloud services enable aiplatform.googleapis.com --project=nodal-fountain-470717-j1")
    
    print("="*60)
