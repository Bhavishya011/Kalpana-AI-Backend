# KalpanaAI Backend 🎨🤖

## Overview
KalpanaAI Backend is an AI-powered storytelling and image enhancement platform designed specifically for artisans. It combines multiple AI agents to create compelling marketing content, enhance product photos, and generate personalized stories that connect artisans with their customers.

## 🚀 Features

### AI Agents Architecture
- **🖼️ Image Generator Agent** - Creates story-driven visuals using Vertex AI Imagen 4.0
- **📖 Storyteller Agent** - Crafts compelling narratives using Gemini 2.0 Flash
- **🎭 Curator Agent** - Enhances product photos with AI-powered editing
- **🎨 Synthesizer Agent** - Combines content into cohesive marketing kits
- **🎼 Orchestrator** - Coordinates all agents for seamless workflows

### Core Capabilities
- **Photo Enhancement** - AI-powered product photo optimization
- **Story Generation** - Personalized narrative creation
- **Image Creation** - AI-generated marketing visuals
- **Social Media Posts** - Ready-to-use promotional content
- **Marketing Kits** - Complete content packages

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python)
- **AI Models**: 
  - Google Vertex AI Imagen 4.0 (Image Generation)
  - Gemini 2.0 Flash (Text Generation)
  - Google Vision API (Image Analysis)
- **Database**: Google Firestore
- **Deployment**: Google Cloud Platform
- **Authentication**: Google Cloud IAM

## 📁 Project Structure

```
.
├── Agents/                     # AI Agent implementations
│   ├── agents/
│   │   ├── curator_agent.py    # Photo enhancement agent
│   │   ├── image_generator_agent.py  # AI image generation
│   │   ├── storyteller_agent.py     # Story creation agent
│   │   ├── synthesizer_agent.py     # Content synthesis
│   │   └── orchestrator.py          # Agent coordination
│   ├── storytelling_kit/       # Generated content samples
│   └── test_*.py              # Agent testing scripts
├── api/                       # FastAPI server implementations
│   ├── main2.0.py            # Primary server (recommended)
│   ├── working_main.py       # Stable fallback
│   └── *.py                  # Various server versions
├── app.yaml                  # Google Cloud deployment config
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Cloud Project with billing enabled
- Vertex AI API enabled
- Firestore database configured

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bhavishya011/Kalpana-AI-Backend.git
   cd Kalpana-AI-Backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth application-default login
   ```

4. **Update project configurations**
   - Edit `Agents/agents/image_generator_agent.py` - Update project ID
   - Edit `Agents/agents/curator_agent.py` - Update project ID
   - Edit `app.yaml` - Update GOOGLE_CLOUD_PROJECT

### Running the Server

**Primary Server (Recommended)**
```bash
cd api
python main2.0.py
```

**Development Server**
```bash
uvicorn main2.0:app --reload --host 0.0.0.0 --port 8000
```

**Server will be available at:**
- 🌐 Main: http://localhost:8000
- 📚 Docs: http://localhost:8000/docs
- ✅ Health: http://localhost:8000/health
- 🎭 Test: http://localhost:8000/test-curator

## 📡 API Endpoints

### Core Endpoints
- `POST /api/storytelling/generate` - Generate complete marketing kit
- `GET /health` - Health check
- `GET /test-curator` - Test image enhancement
- `GET /generated/{asset_id}/{filename}` - Serve generated assets

### Request Format
```json
{
  "product_name": "Traditional Kutch Pottery Vase",
  "description": "Handcrafted ceramic vase with traditional patterns",
  "photo": "base64_encoded_image_data"
}
```

### Response Format
```json
{
  "status": "success",
  "asset_id": "uuid-asset-identifier",
  "marketing_kit": {
    "story_title": "Generated story title",
    "story_text": "Complete narrative",
    "emotional_theme": "warmth",
    "assets": {
      "story_images": ["url1", "url2", "url3"],
      "enhanced_photos": ["enhanced_url1", "enhanced_url2"],
      "social_post": "social_post_url",
      "original_photo": "original_url",
      "image_prompts": ["prompt1", "prompt2"]
    }
  },
  "processing_info": {
    "curator_used": true,
    "enhanced_photos_count": 2,
    "story_images_generated": 3,
    "processing_time_seconds": 45.2
  }
}
```

## 🔧 Configuration

### Required Environment Variables
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

### Project IDs to Update
1. `Agents/agents/image_generator_agent.py` - Line 30
2. `Agents/agents/curator_agent.py` - Line 25
3. `app.yaml` - GOOGLE_CLOUD_PROJECT variable

## 🚀 Deployment

### Google Cloud Run
```bash
gcloud run deploy kalpana-ai-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Google App Engine
```bash
gcloud app deploy app.yaml
```

## 🧪 Testing

### Test Individual Agents
```bash
# Test storyteller
python Agents/test_storyteller_minimal.py

# Test image generation
python Agents/test_story_image_generation.py

# Test curator
python Agents/test_curator_imagen4.py
```

### Test Full Pipeline
```bash
python Agents/run_storytelling_pipeline.py
```

## 📊 Monitoring

### Health Checks
- `/health` - Basic server health
- `/test-curator` - AI agent functionality

### Logging
The server provides comprehensive logging:
- Agent initialization status
- Request processing steps
- Error handling and debugging
- Performance metrics

## 🔍 Troubleshooting

### Common Issues

1. **Billing Error**: Enable billing on Google Cloud Project
2. **API Not Enabled**: Enable Vertex AI and Vision APIs
3. **Authentication**: Run `gcloud auth application-default login`
4. **Quota Exceeded**: Check API quotas in Google Cloud Console

### Error Codes
- `403` - Billing/API access issues
- `429` - Rate limiting
- `500` - Internal agent failures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Create GitHub issues for bugs
- Check documentation at `/docs`
- Review logs for debugging

---

**Built with ❤️ for artisans worldwide** 🎨