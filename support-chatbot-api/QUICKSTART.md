# Quick Start Guide - Support Chatbot API

## 🚀 Deploy in 5 Minutes

### Step 1: Prerequisites
Ensure you have:
- [x] Google Cloud SDK installed
- [x] Logged in: `gcloud auth login`
- [x] Project set: `gcloud config set project nodal-fountain-470717-j1`
- [x] Vertex AI API enabled

### Step 2: Deploy to Cloud Run

**On Linux/Mac:**
```bash
cd support-chatbot-api
chmod +x deploy.sh
./deploy.sh
```

**On Windows (PowerShell):**
```powershell
cd support-chatbot-api
.\deploy.ps1
```

### Step 3: Test Your Deployment

```bash
# Replace YOUR_URL with your Cloud Run URL
curl https://YOUR_URL/health

# Test chat
curl -X POST https://YOUR_URL/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "Hello! What can you help me with?", "language": "en-US"}'
```

### Step 4: Integrate with Frontend

Update `support-center.tsx`:

```typescript
const CHATBOT_API_URL = "https://support-chatbot-api-XXXXX.run.app";

const handleSendMessage = async () => {
  if (!chatMessage.trim()) return;
  
  const userMsg = { role: 'user', message: chatMessage };
  setChatHistory([...chatHistory, userMsg]);
  
  try {
    const response = await fetch(`${CHATBOT_API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: chatMessage,
        session_id: sessionId,
        language: language,
        history: chatHistory
      })
    });
    
    const data = await response.json();
    const botMsg = { role: 'bot', message: data.response };
    setChatHistory([...chatHistory, userMsg, botMsg]);
    setSessionId(data.session_id);
  } catch (error) {
    console.error('Chat error:', error);
    const errorMsg = { 
      role: 'bot', 
      message: 'Sorry, I encountered an error. Please try again.' 
    };
    setChatHistory([...chatHistory, userMsg, errorMsg]);
  }
  
  setChatMessage("");
};
```

## 🧪 Local Testing

### Run Locally
```bash
cd support-chatbot-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
gcloud auth application-default login
python main.py
```

### Test Locally
```bash
# Open browser to http://localhost:8083/docs for interactive API docs

# Or use curl
curl http://localhost:8083/health

curl -X POST http://localhost:8083/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "मुझे मदद चाहिए", "language": "hi-IN"}'
```

## 📊 Monitor Your Deployment

### View Logs
```bash
gcloud run services logs read support-chatbot-api \
  --region us-central1 \
  --limit 50
```

### Check Metrics
Visit: https://console.cloud.google.com/run

## 🔧 Troubleshooting

### Issue: "Permission denied"
```bash
gcloud auth application-default login
gcloud projects add-iam-policy-binding nodal-fountain-470717-j1 \
  --member="user:YOUR_EMAIL" \
  --role="roles/run.admin"
```

### Issue: "Vertex AI not enabled"
```bash
gcloud services enable aiplatform.googleapis.com --project=nodal-fountain-470717-j1
```

### Issue: "Build failed"
Check Dockerfile and ensure all files are present:
- main.py
- requirements.txt
- Dockerfile

### Issue: "Chat responses in wrong language"
Ensure you're passing the `language` parameter correctly:
```json
{
  "message": "Your message",
  "language": "hi-IN"  // or "en-US", "bn-IN", etc.
}
```

## 🎯 Quick Help Categories

Test these quick help endpoints:

```bash
# Getting Started
curl -X POST "https://YOUR_URL/quick-help?category=getting-started"

# Product Creation
curl -X POST "https://YOUR_URL/quick-help?category=product-creation"

# Artisan Mentor
curl -X POST "https://YOUR_URL/quick-help?category=artisan-mentor"

# Market Pulse
curl -X POST "https://YOUR_URL/quick-help?category=market-pulse"

# The Muse
curl -X POST "https://YOUR_URL/quick-help?category=the-muse"

# Pricing
curl -X POST "https://YOUR_URL/quick-help?category=pricing"

# Languages
curl -X POST "https://YOUR_URL/quick-help?category=languages"

# Support
curl -X POST "https://YOUR_URL/quick-help?category=support"
```

## 🌐 Supported Languages

- `en-US` - English
- `hi-IN` - Hindi (हिन्दी)
- `bn-IN` - Bengali (বাংলা)
- `ta-IN` - Tamil (தமிழ்)
- `te-IN` - Telugu (తెలుగు)
- `mr-IN` - Marathi (मराठी)
- `gu-IN` - Gujarati (ગુજરાતી)
- `kn-IN` - Kannada (ಕನ್ನಡ)
- `ml-IN` - Malayalam (മലയാളം)
- `pa-IN` - Punjabi (ਪੰਜਾਬੀ)

## 💡 Example Conversations

### English
```json
{
  "message": "How do I price my pottery products?",
  "language": "en-US"
}
```

### Hindi
```json
{
  "message": "मुझे अपने उत्पाद के लिए अच्छी तस्वीरें कैसे मिलेंगी?",
  "language": "hi-IN"
}
```

### Bengali
```json
{
  "message": "আমি কীভাবে বাজার চাহিদা জানতে পারি?",
  "language": "bn-IN"
}
```

## 📈 Next Steps

1. ✅ Deploy chatbot (you're here!)
2. 🔗 Integrate with frontend
3. 🧪 Test with real users
4. 📊 Monitor usage and feedback
5. 🔄 Iterate and improve

## 🆘 Need Help?

- 📖 Read full [README.md](README.md)
- 🐛 Check logs: `gcloud run services logs read support-chatbot-api`
- 💬 Contact: dev@kalpana-ai.com
- 📚 Docs: https://docs.kalpana-ai.com

---

**Congratulations!** 🎉 Your AI support chatbot is now live and ready to help artisans!
