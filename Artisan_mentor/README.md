# 🎓 Artisan Mentor API

> Comprehensive AI tutor API that transforms traditional artisans into global entrepreneurs through personalized, multimodal learning journeys.

## ✨ Features

- **🌟 Personalized Learning Journeys** - Adapts to each artisan's skill level, learning style, and craft
- **📚 Progressive Curriculum** - 4 levels from Foundation to Global Expansion with increasing difficulty
- **🎯 Multimodal Support** - Text, voice, images in 9 Indian languages
- **🏆 Advanced Gamification** - Points, badges, skill matrix, business metrics
- **☁️ Enterprise Ready** - Full Google Cloud integration with Firestore, Storage, Speech, Translate
- **🔊 Voice Interfaces** - Text-to-speech and speech-to-text for low-literacy users
- **🤖 AI-Powered Validation** - Intelligent feedback on lesson submissions
- **📊 Business Dashboard** - Comprehensive progress and business metrics tracking

## 🏗️ Architecture

```
Artisan_mentor/
├── artisan_mentor/          # Core package
│   ├── agent.py            # Agent wrapper (no ADK dependency)
│   ├── tools.py            # Tool function definitions
│   ├── tutor.py            # HybridArtisanTutor class implementation
│   ├── data/
│   │   └── curriculum.json # Progressive curriculum structure
│   └── __init__.py
├── api_main.py             # FastAPI REST API wrapper
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container configuration
├── deploy.ps1              # Cloud Run deployment script
├── test_api.py             # Comprehensive test suite
├── .env                    # Environment configuration
└── README.md               # This file
```

## 📋 Prerequisites

- Python 3.11+
- Google Cloud Project with the following APIs enabled:
  - Cloud Run
  - Vertex AI
  - Cloud Storage
  - Firestore
  - Cloud Speech
  - Cloud Text-to-Speech
  - Cloud Translation
  - Cloud Vision
- Google Cloud CLI (`gcloud`) installed and authenticated

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Google Cloud settings
   ```

3. **Run tests:**
   ```bash
   python test_api.py
   ```

4. **Start the API locally:**
   ```bash
   uvicorn api_main:app --reload --port 8080
   ```

5. **Access the API:**
   - API: http://localhost:8080
   - Interactive Docs: http://localhost:8080/docs
   - Health Check: http://localhost:8080/health

### Cloud Deployment

1. **Deploy to Cloud Run:**
   ```powershell
   .\deploy.ps1
   ```

2. **Test the deployed API:**
   ```bash
   curl https://[YOUR-SERVICE-URL]/health
   ```

## 📡 API Endpoints

### Core Endpoints

#### `POST /start-journey`
Start a personalized learning journey for an artisan.

**Request:**
```json
{
  "user_id": "user_123",
  "name": "Priya Sharma",
  "learning_style": "visual",
  "language": "en",
  "current_skill_level": "beginner",
  "craft_analysis": {
    "craft_name": "Madhubani Painting",
    "region": "Bihar"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "user_id": "user_123",
  "welcome_message": "Welcome Priya! Let's begin...",
  "starting_point": {
    "module": "foundation",
    "lesson": "F1.1"
  }
}
```

#### `POST /get-lesson`
Get an interactive lesson with multimodal content.

**Request:**
```json
{
  "user_id": "user_123",
  "lesson_id": "F1.1",
  "format": "multimodal"
}
```

#### `POST /submit-work`
Submit lesson work for AI-powered validation.

**Request:**
```json
{
  "user_id": "user_123",
  "lesson_id": "F1.1",
  "submission": {
    "content": "My 5 professional craft photos...",
    "images": ["url1", "url2", "url3"]
  }
}
```

#### `POST /dashboard`
Get comprehensive business and learning dashboard.

**Request:**
```json
{
  "user_id": "user_123"
}
```

#### `POST /analyze-craft`
Analyze a craft image for comprehensive insights.

**Request:**
- Upload image file OR provide GCS URI

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "craft_name": "Madhubani Painting",
    "materials": ["natural dyes", "paper"],
    "techniques": ["line work", "geometric patterns"],
    "target_markets": ["art collectors", "interior design"],
    "export_potential": "High - unique cultural appeal"
  }
}
```

### Voice Endpoints

#### `POST /tts`
Convert text to speech in multiple languages.

**Request:**
```json
{
  "text": "Welcome to your learning journey!",
  "language": "hi"
}
```

#### `POST /stt`
Convert speech to text.

**Request:**
```json
{
  "audio_uri": "gs://bucket/audio.mp3",
  "language": "hi"
}
```

## 📚 Curriculum Structure

### 1. 🎯 Foundation Builder (Beginner)
- **F1.1** - Craft Photography Mastery
- **F1.2** - Your Origin Story

### 2. 🛒 Marketplace Pro (Intermediate)
- **M2.1** - SEO Listing Optimization
- **M2.2** - Advanced Pricing Strategy

### 3. 📈 Digital Growth Engine (Advanced)
- **D3.1** - Social Media Funnel
- **D3.2** - Micro-Budget Ad Campaigns

### 4. 🌍 Global Business Scale (Expert)
- **G4.1** - International Export Mastery
- **G4.2** - Business Scaling & Team Building

## 🌐 Supported Languages

- 🇬🇧 English (en)
- 🇮🇳 Hindi (hi)
- 🇮🇳 Tamil (ta)
- 🇮🇳 Telugu (te)
- 🇮🇳 Kannada (kn)
- 🇮🇳 Malayalam (ml)
- 🇮🇳 Bengali (bn)
- 🇮🇳 Marathi (mr)
- 🇮🇳 Gujarati (gu)

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

**Test Coverage:**
- ✅ Module imports
- ✅ Agent structure
- ✅ Learning journey creation
- ✅ API wrapper functionality
- ✅ Curriculum loading

## 🔧 Configuration

Environment variables (`.env`):

```bash
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
CLOUD_STORAGE_BUCKET="kalpana-artisan-tutor"

# Feature Flags
ENABLE_VOICE_INTERFACE="true"
ENABLE_MULTILINGUAL="true"
ENABLE_ADAPTIVE_LEARNING="true"
ENABLE_AI_VALIDATION="true"

# Supported Languages
SUPPORTED_LANGUAGES="en,hi,ta,te,kn,ml,bn,mr,gu"
```

## 📊 Google Cloud Resources Required

1. **Firestore Database** - Store user profiles, progress, achievements
2. **Cloud Storage Bucket** - Store audio files, images
3. **Vertex AI** - Gemini 2.0 Flash for AI-powered analysis
4. **Cloud Speech** - Speech-to-text in multiple languages
5. **Cloud Text-to-Speech** - Text-to-speech in multiple languages
6. **Cloud Translation** - Multilingual support
7. **Cloud Vision** - Image analysis

## 🚀 Deployment

### Cloud Run Configuration

- **Memory:** 4GB
- **CPU:** 2
- **Timeout:** 600 seconds (10 minutes)
- **Concurrency:** Default
- **Authentication:** Allow unauthenticated

### Deploy Command

```powershell
.\deploy.ps1
```

This script will:
1. Build the container image
2. Push to Google Container Registry
3. Deploy to Cloud Run
4. Configure environment variables
5. Display the service URL

## 🎯 Use Cases

### For Artisans
- Learn business skills at their own pace
- Get personalized guidance based on their craft
- Access lessons in their native language
- Track progress and earn achievements

### For Organizations
- Train multiple artisans at scale
- Track collective progress
- Identify growth opportunities
- Measure business impact

### For Platforms
- Integrate AI tutoring into marketplace platforms
- Provide value-added services to artisans
- Improve seller success rates
- Build community learning programs

## 📈 Metrics & Analytics

The dashboard provides:
- **Learning Progress** - Completed lessons, current streak, skill level
- **Business Metrics** - Products listed, sales, social media presence
- **Skill Development** - Photography, storytelling, marketing, pricing scores
- **Achievements** - Unlocked badges, milestones reached
- **Recommendations** - Personalized next steps

## 🤝 Integration Example

### Start a Journey

```python
import requests

response = requests.post(
    "https://artisan-mentor-api-[PROJECT].run.app/start-journey",
    json={
        "user_id": "artisan_001",
        "name": "Lakshmi",
        "learning_style": "visual",
        "language": "ta",
        "current_skill_level": "beginner"
    }
)

data = response.json()
print(f"Welcome: {data['welcome_message']}")
```

## 🔒 Security

- All API calls use HTTPS
- Google Cloud IAM for service authentication
- CORS configured for specific origins
- Rate limiting recommended for production

## 📝 License

Proprietary - Part of KalpanaAI Platform

## 👥 Support

For issues or questions:
- Create an issue in the repository
- Contact: support@kalpanaai.com

## 🎉 Acknowledgments

Built with:
- FastAPI
- Google Cloud Platform
- Vertex AI (Gemini 2.0 Flash)
- Imagen 4.0
- Cloud Speech & Text-to-Speech

---

**Ready to empower artisans! 🚀**
