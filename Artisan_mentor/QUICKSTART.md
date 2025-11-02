# 🚀 Artisan Mentor - Quick Start Guide

## What You've Got

A **complete AI-powered tutoring system** for artisan business education:
- ✅ **12 lessons** across 4 difficulty levels (Beginner → Expert)
- ✅ **585 total points** to earn
- ✅ **9 Indian languages** supported
- ✅ **AI-powered validation** with Gemini 2.0 Flash
- ✅ **Voice interfaces** for accessibility
- ✅ **Comprehensive dashboard** with business metrics
- ✅ **Production-ready** REST API

## Deploy in 2 Minutes

```powershell
# Navigate to directory
cd Artisan_mentor

# Deploy to Cloud Run (builds + deploys automatically)
.\deploy.ps1
```

That's it! The script will:
1. ✅ Build Docker container
2. ✅ Push to Google Container Registry  
3. ✅ Deploy to Cloud Run
4. ✅ Configure 4GB RAM, 2 CPU, 10min timeout
5. ✅ Return your service URL

## Test Your API

```bash
# Health check
curl https://artisan-mentor-api-[PROJECT-ID].us-central1.run.app/health

# Start a journey
curl -X POST https://artisan-mentor-api-[PROJECT-ID].us-central1.run.app/start-journey \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priya Sharma",
    "learning_style": "visual",
    "language": "en",
    "current_skill_level": "beginner"
  }'
```

## API Documentation

Once deployed, visit:
```
https://artisan-mentor-api-[PROJECT-ID].us-central1.run.app/docs
```

Interactive Swagger UI with all endpoints and schemas!

## The Learning Journey

### 🎯 Level 1: Foundation (3 lessons, 85 pts)
Artisans learn:
- Professional craft photography
- Compelling origin storytelling  
- Accurate cost calculation

**Outcome**: Ready to showcase products professionally

### 🛒 Level 2: Marketplace Pro (3 lessons, 120 pts)
Artisans learn:
- SEO-optimized product listings
- 3-tier pricing strategies
- Memorable packaging design

**Outcome**: Ready to sell on multiple platforms

### 📈 Level 3: Digital Growth (3 lessons, 155 pts)
Artisans learn:
- Social media content strategy
- Micro-budget advertising
- Video marketing basics

**Outcome**: Active digital presence, customer acquisition

### 🌍 Level 4: Global Scale (3 lessons, 225 pts)
Artisans learn:
- International export processes
- Business scaling & team building
- Comprehensive brand building

**Outcome**: Global entrepreneur ready

## Integration with KalpanaAI

```typescript
// In your frontend
const API_URL = "https://artisan-mentor-api-[PROJECT-ID].us-central1.run.app";

// Start journey
const response = await fetch(`${API_URL}/start-journey`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: currentUser.id,
    name: currentUser.name,
    learning_style: "visual",
    language: "en",
    current_skill_level: "beginner"
  })
});

const data = await response.json();
console.log(data.welcome_message);
console.log(data.starting_point); // { module: "foundation", lesson: "F1.1" }
```

## Key Features to Highlight

### 1. AI-Powered Validation
Every submission gets intelligent feedback:
- Detailed scoring (0-100%)
- Identified strengths
- Specific improvements
- Pass/fail with reasoning

### 2. Progressive Curriculum
- 12 lessons building on each other
- Beginner → Expert progression
- Real business outcomes at every step
- 585 total points to earn

### 3. Comprehensive Dashboard
Artisans see:
- Learning progress (completion %, points, streak)
- Business readiness scores
- Skill matrix (10 tracked skills)
- Revenue impact estimates
- Growth opportunities

### 4. Multilingual + Voice
- 9 Indian languages
- Text-to-speech for lessons
- Speech-to-text for submissions
- Low-literacy accessibility

## Example User Flow

```javascript
// 1. Artisan signs up
POST /start-journey
→ Gets welcome message, starting lesson ID

// 2. Gets first lesson
POST /get-lesson { user_id, lesson_id: "F1.1" }
→ Gets personalized craft photography guidance

// 3. Completes lesson
POST /submit-work { 
  user_id, 
  lesson_id: "F1.1",
  submission: { content: "My 5 photos...", images: [...] }
}
→ Gets AI feedback, points, next lesson

// 4. Checks progress
POST /dashboard { user_id }
→ Gets full dashboard with metrics, recommendations
```

## Architecture

```
Frontend (KalpanaAI)
    ↓
FastAPI REST API (Cloud Run)
    ↓
HybridArtisanTutor (Core Logic)
    ↓
┌─────────────────────────────┐
│  Gemini 2.0 Flash (AI)      │
│  Firestore (User Data)      │
│  Cloud Storage (Media)      │
│  Cloud Speech (Voice)       │
│  Cloud Vision (Images)      │
└─────────────────────────────┘
```

## What Makes This Special

1. **Only AI tutor specifically for artisans**
   - Not generic business education
   - Craft-specific personalization
   - Cultural sensitivity built-in

2. **Progressive & gamified**
   - Clear progression path
   - Points, badges, achievements
   - Visible business impact

3. **Voice-first accessibility**
   - Supports low-literacy users
   - 9 Indian languages
   - Audio lessons & submissions

4. **Business outcome focused**
   - Every lesson = revenue impact
   - Tracks readiness metrics
   - Identifies growth opportunities

5. **Production-ready**
   - Full error handling
   - Scalable architecture
   - Comprehensive testing
   - Cloud Run deployment

## Monitoring & Maintenance

Once deployed:

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=artisan-mentor-api" --limit 50

# Check metrics
gcloud monitoring dashboards list

# Update deployment
.\deploy.ps1  # Rebuilds and redeploys
```

## Costs Estimate

**Google Cloud Run**:
- Free tier: 2M requests/month
- Typical: $0.40 per million requests
- Memory: $0.0000025 per GB-second

**Vertex AI (Gemini)**:
- Input: $0.075 per 1M tokens
- Output: $0.30 per 1M tokens

**Estimated**: $10-50/month for 1000 active users

## Support

- 📖 Full documentation in `README.md`
- 🧪 Test suite in `test_api.py`
- 📊 Architecture in `IMPLEMENTATION_COMPLETE.md`
- 🐛 Issues: GitHub repo

## Next Steps

1. **Deploy** ✅ Run `.\deploy.ps1`
2. **Test** ✅ Check `/health` and `/docs`
3. **Integrate** ✅ Connect to KalpanaAI frontend
4. **Launch** ✅ Onboard first artisans
5. **Monitor** ✅ Track usage and feedback

---

**You're ready to transform artisan education! 🚀**

Deploy now and start empowering artisans to become global entrepreneurs.
