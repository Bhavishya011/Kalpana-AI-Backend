"""
Initialize Firestore database with proper structure and sample data.
Run this once to set up your database.
"""

from google.cloud import firestore
import os
from datetime import datetime

# Set your project ID
os.environ['GOOGLE_CLOUD_PROJECT'] = 'nodal-fountain-470717-j1'

db = firestore.Client()

def create_firestore_structure():
    """Create initial Firestore structure with sample data."""
    
    print("🔧 Setting up Firestore database structure...\n")
    
    # Sample user for testing
    sample_user_id = "test_artisan_001"
    
    # 1. Create user profile
    print("1️⃣ Creating user profile...")
    user_ref = db.collection('users').document(sample_user_id)
    user_ref.set({
        'profile': {
            'user_id': sample_user_id,
            'name': 'Meera Devi',
            'learning_style': 'visual',
            'language': 'hi',
            'current_skill_level': 'beginner',
            'craft_analysis': {
                'craft_name': 'Madhubani Painting',
                'region': 'Bihar',
                'materials': ['natural dyes', 'paper', 'brushes'],
                'skill_level_required': 'Beginner'
            }
        },
        'learning_journey': {
            'current_module': 'foundation',
            'current_lesson': 'F1.1',
            'completed_modules': [],
            'learning_style': 'visual',
            'language_preference': 'hi',
            'created_at': datetime.now(),
            'last_active': datetime.now(),
            'personalized_curriculum': {
                'starting_module': 'foundation',
                'starting_lesson': 'F1.1'
            }
        },
        'progress_metrics': {
            'total_points': 0,
            'current_streak': 0,
            'completed_lessons': 0,
            'skill_level': 'beginner'
        },
        'achievements': {
            'unlocked': [],
            'in_progress': [],
            'next_milestones': ['F1.1']
        }
    })
    print("   ✅ User profile created\n")
    
    # 2. Create curriculum index
    print("2️⃣ Creating curriculum index...")
    curriculum_ref = db.collection('curriculum').document('structure')
    curriculum_ref.set({
        'total_modules': 4,
        'total_lessons': 12,
        'total_points': 585,
        'modules': {
            'foundation': {
                'title': '🎯 Foundation Builder',
                'level': 'beginner',
                'lessons': 3,
                'total_points': 85
            },
            'marketplace_ready': {
                'title': '🛒 Marketplace Pro',
                'level': 'intermediate',
                'lessons': 3,
                'total_points': 120
            },
            'digital_marketing': {
                'title': '📈 Digital Growth Engine',
                'level': 'advanced',
                'lessons': 3,
                'total_points': 155
            },
            'global_expansion': {
                'title': '🌍 Global Business Scale',
                'level': 'expert',
                'lessons': 3,
                'total_points': 225
            }
        },
        'updated_at': datetime.now()
    })
    print("   ✅ Curriculum index created\n")
    
    # 3. Create system stats
    print("3️⃣ Creating system stats...")
    stats_ref = db.collection('system').document('stats')
    stats_ref.set({
        'total_users': 1,
        'active_users': 1,
        'total_submissions': 0,
        'total_completions': 0,
        'total_points_awarded': 0,
        'average_completion_rate': 0,
        'updated_at': datetime.now()
    })
    print("   ✅ System stats created\n")
    
    print("✅ Database setup complete!")
    print(f"\n📊 Sample user created: {sample_user_id}")
    print(f"🔗 View in Firebase Console:")
    print(f"   https://console.firebase.google.com/project/nodal-fountain-470717-j1/firestore")
    
    return sample_user_id

def create_security_rules():
    """Print Firestore security rules to be applied."""
    
    rules = """
// Firestore Security Rules for Artisan Mentor
// Copy and paste these into Firebase Console > Firestore > Rules

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }
    
    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }
    
    // Users collection
    match /users/{userId} {
      // Allow unauthenticated read/write for API access
      // In production, use proper authentication
      allow read, write: if true;
    }
    
    // Curriculum collection (read-only for all)
    match /curriculum/{docId} {
      allow read: if true;
      allow write: if false; // Only admins via backend
    }
    
    // System stats (read-only)
    match /system/{docId} {
      allow read: if true;
      allow write: if false;
    }
    
    // Craft analyses
    match /craft_analyses/{docId} {
      allow read, write: if true;
    }
  }
}
"""
    
    print("\n" + "="*60)
    print("📋 FIRESTORE SECURITY RULES")
    print("="*60)
    print(rules)
    print("="*60)
    print("\n⚠️  Apply these rules in Firebase Console:")
    print("1. Go to: https://console.firebase.google.com/project/nodal-fountain-470717-j1/firestore/rules")
    print("2. Copy the rules above")
    print("3. Paste and click 'Publish'\n")

if __name__ == "__main__":
    try:
        # Create database structure
        sample_user = create_firestore_structure()
        
        # Print security rules
        create_security_rules()
        
        print("\n✨ Next Steps:")
        print("1. Apply security rules (see above)")
        print("2. Run: python setup_storage.py")
        print("3. Run: python verify_setup.py")
        print("4. Test with: python test_api.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Enabled Firestore API: gcloud services enable firestore.googleapis.com --project=nodal-fountain-470717-j1")
        print("2. Created Firestore database (Native mode)")
        print("3. Authenticated with: gcloud auth application-default login")
