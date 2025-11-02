# KalpanaAI Support Chatbot API

An AI-powered support chatbot built with Gemini 2.5 Flash, providing comprehensive assistance for KalpanaAI platform users.

## Features

- 🤖 **Powered by Gemini 2.5 Flash** - Latest Google AI model
- 🌍 **Multilingual Support** - Responds in 10+ Indian languages
- 📚 **Comprehensive Knowledge** - Full knowledge of all KalpanaAI features
- 💬 **Context-Aware** - Maintains conversation history
- ⚡ **Fast & Scalable** - Deployed on Google Cloud Run
- 🎯 **Quick Help** - Pre-defined responses for common questions

## Knowledge Base Coverage

### Platform Features
- AI-Powered Product Creation
- Market Pulse (Market Intelligence)
- The Muse (Creative AI Assistant)
- Artisan Mentor (Learning Platform)
- Sales Analytics
- Multilingual Support

### Craft Categories
- Traditional Textiles
- Pottery & Ceramics
- Jewelry & Accessories
- Home Decor
- Paintings & Art
- Woodwork & Furniture
- Metalwork
- Handmade Bags
- Traditional Toys
- Embroidery

### Regional & Cultural Knowledge
- Indian festivals (Diwali, Holi, Durga Puja, etc.)
- Regional craft specialties
- Traditional techniques
- Seasonal opportunities

## API Endpoints

### `POST /chat`
Main chat endpoint for conversations

**Request:**
```json
{
  "message": "How do I create a product?",
  "session_id": "optional-session-id",
  "language": "en-US",
  "history": [
    {
      "role": "user",
      "content": "Previous message",
      "timestamp": "2025-01-01T12:00:00"
    }
  ]
}
```

**Response:**
```json
{
  "response": "To create a product on KalpanaAI...",
  "session_id": "session_1234567890",
  "timestamp": "2025-01-01T12:00:00",
  "language": "en-US"
}
```

### `POST /quick-help`
Get quick responses for common categories

**Categories:**
- `getting-started`
- `product-creation`
- `artisan-mentor`
- `market-pulse`
- `the-muse`
- `pricing`
- `languages`
- `support`

**Example:**
```bash
curl -X POST "https://your-api-url/quick-help?category=product-creation"
```

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T12:00:00",
  "active_sessions": 5,
  "model": "gemini-2.0-flash-exp",
  "project": "kalpana-ai"
}
```

### `POST /chat/reset`
Reset a chat session

**Request:**
```bash
curl -X POST "https://your-api-url/chat/reset?session_id=session_123"
```

## Local Development

### Prerequisites
- Python 3.11+
- Google Cloud SDK
- Vertex AI API enabled
- Application Default Credentials configured

### Setup

1. **Clone and navigate to directory:**
```bash
cd support-chatbot-api
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up Google Cloud credentials:**
```bash
gcloud auth application-default login
gcloud config set project nodal-fountain-470717-j1
```

5. **Create .env file:**
```bash
cp .env.example .env
```

6. **Run locally:**
```bash
python main.py
```

API will be available at: http://localhost:8083

## Deployment to Cloud Run

### One-Command Deployment

```bash
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment

1. **Build Docker image:**
```bash
gcloud builds submit --tag gcr.io/nodal-fountain-470717-j1/support-chatbot-api
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy support-chatbot-api \
  --image gcr.io/nodal-fountain-470717-j1/support-chatbot-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10
```

3. **Get service URL:**
```bash
gcloud run services describe support-chatbot-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

## Integration with Frontend

### Update Support Center Component

```typescript
// In support-center.tsx

const handleSendMessage = async () => {
  if (!chatMessage.trim()) return;
  
  // Add user message to history
  const userMessage = { role: 'user', message: chatMessage };
  setChatHistory([...chatHistory, userMessage]);
  
  // Call API
  const response = await fetch('https://your-api-url/chat', {
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
  
  // Add bot response to history
  const botMessage = { role: 'bot', message: data.response };
  setChatHistory([...chatHistory, userMessage, botMessage]);
  
  setChatMessage("");
};
```

## Testing

### Test Chat Endpoint
```bash
curl -X POST https://your-api-url/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "मुझे एक उत्पाद बनाने में मदद चाहिए",
    "language": "hi-IN"
  }'
```

### Test Quick Help
```bash
curl -X POST "https://your-api-url/quick-help?category=pricing"
```

### Test Health
```bash
curl https://your-api-url/health
```

## Example Conversations

### English
```
User: How do I create my first product?
Bot: To create your first product on KalpanaAI: 1) Click "Add Product" 
     from the dashboard, 2) Upload clear photos of your craft...
```

### Hindi
```
User: मुझे बाजार की जानकारी कैसे मिलेगी?
Bot: Market Pulse सुविधा का उपयोग करें। यह आपको अलग-अलग क्षेत्रों में 
     मांग के बारे में जानकारी देती है...
```

### Bengali
```
User: আমি কিভাবে মূল্য নির্ধারণ করব?
Bot: Smart Pricing ব্যবহার করুন যা বাজার চাহিদা, উপাদান খরচ এবং 
     প্রতিযোগীদের মূল্যের উপর ভিত্তি করে সুপারিশ করে...
```

## Monitoring

### View Logs
```bash
gcloud run services logs read support-chatbot-api \
  --region us-central1 \
  --limit 50
```

### Monitor Metrics
- Visit Cloud Console → Cloud Run → support-chatbot-api
- Check: Request count, Latency, Error rate, Active instances

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_CLOUD_PROJECT` | GCP Project ID | `kalpana-ai` |
| `GOOGLE_CLOUD_LOCATION` | Vertex AI location | `us-central1` |
| `PORT` | Server port | `8083` |

## Architecture

```
┌─────────────┐
│   Frontend  │
│  (Next.js)  │
└──────┬──────┘
       │
       │ POST /chat
       ▼
┌─────────────────┐
│  Support Bot    │
│   (FastAPI)     │
└────────┬────────┘
         │
         │ Vertex AI
         ▼
┌─────────────────┐
│  Gemini 2.5     │
│     Flash       │
└─────────────────┘
```

## Features in Detail

### Context Awareness
- Maintains last 5 messages for context
- Session-based conversation tracking
- Remembers user preferences

### Multilingual Intelligence
- Auto-detects user language
- Responds in same language
- Supports code-switching

### Knowledge Depth
- 2000+ words of platform knowledge
- Festival calendar integration
- Regional craft specialties
- Traditional knowledge respect

## Cost Optimization

- Uses efficient Gemini 2.5 Flash model
- Scales to zero when idle
- 2GB memory, 2 CPU optimal config
- Max 10 instances for cost control

## Security

- CORS configured for frontend only (update in production)
- No sensitive data in responses
- Session data in memory (use Redis for production)
- Rate limiting recommended

## Future Enhancements

- [ ] Redis for session storage
- [ ] Rate limiting
- [ ] Analytics dashboard
- [ ] A/B testing responses
- [ ] Feedback collection
- [ ] Voice input/output
- [ ] Image understanding
- [ ] Multi-modal responses

## Support

For issues or questions:
- GitHub Issues
- Email: dev@kalpana-ai.com
- Documentation: docs.kalpana-ai.com

## License

Proprietary - KalpanaAI Platform

---

Built with ❤️ for Indian Artisans
