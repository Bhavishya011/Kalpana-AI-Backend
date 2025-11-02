"""
Set up Cloud Storage buckets for Artisan Mentor.
Run this once to create and configure storage buckets.
"""

from google.cloud import storage
import json
import os

PROJECT_ID = 'nodal-fountain-470717-j1'
BUCKET_NAME = 'kalpana-artisan-tutor'

def create_storage_bucket():
    """Create GCS bucket with proper configuration."""
    
    print("🪣 Setting up Cloud Storage...\n")
    
    storage_client = storage.Client(project=PROJECT_ID)
    
    # Check if bucket exists
    bucket = storage_client.bucket(BUCKET_NAME)
    
    try:
        if not bucket.exists():
            print(f"Creating bucket: {BUCKET_NAME}")
            bucket = storage_client.create_bucket(
                BUCKET_NAME,
                location='us-central1'
            )
            print(f"✅ Bucket created: {BUCKET_NAME}\n")
        else:
            print(f"✅ Bucket already exists: {BUCKET_NAME}\n")
    except Exception as e:
        print(f"Error checking/creating bucket: {e}")
        print("Creating bucket anyway...")
        bucket = storage_client.bucket(BUCKET_NAME)
    
    # Set CORS configuration
    print("⚙️  Configuring CORS...")
    try:
        bucket.cors = [
            {
                "origin": ["*"],
                "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
                "responseHeader": ["Content-Type", "Access-Control-Allow-Origin"],
                "maxAgeSeconds": 3600
            }
        ]
        bucket.patch()
        print("✅ CORS configured\n")
    except Exception as e:
        print(f"⚠️  CORS configuration warning: {e}\n")
    
    # Make bucket publicly readable
    print("🔓 Setting public access...")
    try:
        policy = bucket.get_iam_policy(requested_policy_version=3)
        policy.bindings.append({
            "role": "roles/storage.objectViewer",
            "members": {"allUsers"}
        })
        bucket.set_iam_policy(policy)
        print("✅ Public access enabled\n")
    except Exception as e:
        print(f"⚠️  Public access warning: {e}\n")
    
    # Create folder structure
    print("📁 Creating folder structure...")
    folders = [
        'audio/lessons/',
        'audio/submissions/',
        'images/submissions/',
        'images/profiles/',
        'documents/',
        'temp/'
    ]
    
    for folder in folders:
        try:
            blob = bucket.blob(folder + '.gitkeep')
            blob.upload_from_string('')
            print(f"   ✅ Created: {folder}")
        except Exception as e:
            print(f"   ⚠️  {folder}: {e}")
    
    print(f"\n✅ Storage setup complete!")
    print(f"🔗 Bucket URL: gs://{BUCKET_NAME}")
    print(f"🌐 Public URL: https://storage.googleapis.com/{BUCKET_NAME}")
    
    return BUCKET_NAME

def save_cors_config():
    """Save CORS configuration to file."""
    cors_config = [{
        "origin": ["*"],
        "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
        "responseHeader": ["Content-Type", "Access-Control-Allow-Origin"],
        "maxAgeSeconds": 3600
    }]
    
    os.makedirs('config', exist_ok=True)
    with open('config/cors.json', 'w') as f:
        json.dump(cors_config, f, indent=2)
    
    print(f"\n💾 CORS config saved to: config/cors.json")
    print("\nTo apply CORS manually:")
    print(f"gsutil cors set config/cors.json gs://{BUCKET_NAME}")

if __name__ == "__main__":
    try:
        bucket_name = create_storage_bucket()
        save_cors_config()
        
        print("\n✨ Storage is ready!")
        print(f"\nTest upload:")
        print(f"  echo 'test' > test.txt")
        print(f"  gsutil cp test.txt gs://{bucket_name}/temp/")
        print(f"  gsutil rm gs://{bucket_name}/temp/test.txt")
        
        print("\n📝 Next Steps:")
        print("1. Run: python verify_setup.py")
        print("2. Run: python test_api.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Enabled Cloud Storage API: gcloud services enable storage.googleapis.com --project=nodal-fountain-470717-j1")
        print("2. Authenticated with: gcloud auth application-default login")
