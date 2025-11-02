# API Documentation

## Base URL
```
Production: https://support-chatbot-api-XXXXX.run.app
Local: http://localhost:8083
```

## Authentication
Currently no authentication required. In production, consider adding API keys or OAuth.

---

## Endpoints

### 1. Root Endpoint
Get API information

**Endpoint**: `GET /`

**Response**:
```json
{
  "service": "KalpanaAI Support Chatbot",
  "version": "1.0.0",
  "model": "gemini-2.0-flash-exp",
  "status": "active"
}
```

---

### 2. Health Check
Check API health and status

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T12:00:00.000000",
  "active_sessions": 3,
  "model": "gemini-2.0-flash-exp",
  "project": "nodal-fountain-470717-j1"
}
```

---

### 3. Chat
Main conversational endpoint

**Endpoint**: `POST /chat`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "How do I create a product?",
  "session_id": "optional-session-id",
  "language": "en-US",
  "history": [
    {
      "role": "user",
      "content": "Previous user message",
      "timestamp": "2025-01-01T11:00:00"
    },
    {
      "role": "bot",
      "content": "Previous bot response",
      "timestamp": "2025-01-01T11:00:05"
    }
  ]
}
```

**Parameters**:
- `message` (required, string): User's message
- `session_id` (optional, string): Session identifier for context
- `language` (optional, string): Language code (default: "en-US")
- `history` (optional, array): Conversation history (last 5 messages used)

**Response**:
```json
{
  "response": "To create a product on KalpanaAI...",
  "session_id": "session_1735738800.123456",
  "timestamp": "2025-01-01T12:00:00.000000",
  "language": "en-US"
}
```

**Example cURL**:
```bash
curl -X POST https://your-api-url/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "What is The Muse?",
    "language": "en-US"
  }'
```

**Example PowerShell**:
```powershell
$body = @{
    message = "What is The Muse?"
    language = "en-US"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://your-api-url/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

**Example JavaScript**:
```javascript
const response = await fetch('https://your-api-url/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "What is The Muse?",
    language: "en-US"
  })
});

const data = await response.json();
console.log(data.response);
```

---

### 4. Quick Help
Get pre-defined quick responses

**Endpoint**: `POST /quick-help`

**Query Parameters**:
- `category` (required, string): Help category

**Valid Categories**:
- `getting-started`
- `product-creation`
- `artisan-mentor`
- `market-pulse`
- `the-muse`
- `pricing`
- `languages`
- `support`

**Response**:
```json
{
  "category": "product-creation",
  "response": "To create a product: 1) Go to 'Add Product', 2) Upload product images...",
  "timestamp": "2025-01-01T12:00:00.000000"
}
```

**Example cURL**:
```bash
curl -X POST "https://your-api-url/quick-help?category=pricing"
```

**Example JavaScript**:
```javascript
const response = await fetch(
  'https://your-api-url/quick-help?category=pricing',
  { method: 'POST' }
);
const data = await response.json();
console.log(data.response);
```

---

### 5. Reset Session
Clear a chat session

**Endpoint**: `POST /chat/reset`

**Query Parameters**:
- `session_id` (required, string): Session to reset

**Response**:
```json
{
  "message": "Session reset successfully",
  "session_id": "session_123"
}
```

**Example cURL**:
```bash
curl -X POST "https://your-api-url/chat/reset?session_id=session_123"
```

---

### 6. List Sessions
Get active chat sessions

**Endpoint**: `GET /chat/sessions`

**Response**:
```json
{
  "active_sessions": 5,
  "session_ids": [
    "session_1735738800.123",
    "session_1735738900.456",
    "session_1735739000.789"
  ]
}
```

**Example cURL**:
```bash
curl https://your-api-url/chat/sessions
```

---

## Language Codes

| Language | Code | Example |
|----------|------|---------|
| English | `en-US` | "How do I create a product?" |
| Hindi | `hi-IN` | "मुझे उत्पाद कैसे बनाना है?" |
| Bengali | `bn-IN` | "আমি কীভাবে পণ্য তৈরি করব?" |
| Tamil | `ta-IN` | "நான் எப்படி தயாரிப்பு உருவாக்குவது?" |
| Telugu | `te-IN` | "నేను ఉత్పత్తిని ఎలా సృష్టించాలి?" |
| Marathi | `mr-IN` | "मी उत्पादन कसे तयार करू?" |
| Gujarati | `gu-IN` | "હું ઉત્પાદન કેવી રીતે બનાવું?" |
| Kannada | `kn-IN` | "ನಾನು ಉತ್ಪನ್ನವನ್ನು ಹೇಗೆ ರಚಿಸುವುದು?" |
| Malayalam | `ml-IN` | "ഞാൻ എങ്ങനെ ഉൽപ്പന്നം സൃഷ്ടിക്കും?" |
| Punjabi | `pa-IN` | "ਮੈਂ ਉਤਪਾਦ ਕਿਵੇਂ ਬਣਾਵਾਂ?" |

---

## Error Responses

### 400 Bad Request
Invalid request format or parameters

```json
{
  "detail": "Invalid request: message is required"
}
```

### 500 Internal Server Error
Server error during processing

```json
{
  "detail": "Chat error: [error message]"
}
```

---

## Rate Limiting

Currently no rate limiting. Recommended for production:
- 100 requests per minute per IP
- 1000 requests per hour per session

---

## Best Practices

### 1. Session Management
- Generate unique `session_id` for each user
- Reuse `session_id` for continuous conversations
- Reset session when starting new topic

### 2. Conversation History
- Send last 3-5 messages for context
- Include both user and bot messages
- Trim history if token limit approached

### 3. Language Handling
- Always pass `language` parameter
- Match user's selected language
- Handle language switching mid-conversation

### 4. Error Handling
```javascript
try {
  const response = await fetch(API_URL, {
    method: 'POST',
    body: JSON.stringify(data)
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  
  const result = await response.json();
  return result;
} catch (error) {
  console.error('Chat error:', error);
  return {
    response: "Sorry, I'm having trouble connecting. Please try again.",
    error: true
  };
}
```

### 5. Timeout Handling
- Set client timeout to 30 seconds
- Show loading state to user
- Provide retry option on timeout

---

## Example Use Cases

### Use Case 1: New User Onboarding
```javascript
// User asks about getting started
const response = await fetch('/chat', {
  method: 'POST',
  body: JSON.stringify({
    message: "I'm new to KalpanaAI. How do I start?",
    language: "en-US"
  })
});
```

### Use Case 2: Feature-Specific Help
```javascript
// User needs help with Market Pulse
const response = await fetch('/chat', {
  method: 'POST',
  body: JSON.stringify({
    message: "How does Market Pulse work?",
    session_id: userId,
    language: "en-US"
  })
});
```

### Use Case 3: Multilingual Support
```javascript
// Hindi-speaking user
const response = await fetch('/chat', {
  method: 'POST',
  body: JSON.stringify({
    message: "मुझे दिवाली के लिए क्या तैयारी करनी चाहिए?",
    language: "hi-IN"
  })
});
```

### Use Case 4: Follow-up Questions
```javascript
// Conversation with context
const history = [
  { role: "user", content: "What is Artisan Mentor?" },
  { role: "bot", content: "Artisan Mentor is a learning platform..." }
];

const response = await fetch('/chat', {
  method: 'POST',
  body: JSON.stringify({
    message: "How do I earn points?",
    session_id: userId,
    language: "en-US",
    history: history
  })
});
```

### Use Case 5: Quick Information
```javascript
// Get quick help without conversation
const response = await fetch(
  '/quick-help?category=pricing',
  { method: 'POST' }
);
```

---

## Testing

### Interactive API Documentation
Visit: `https://your-api-url/docs`

FastAPI provides interactive Swagger UI for testing all endpoints.

### Test Script
Run the included test script:
```bash
python test_chatbot.py
```

---

## Performance

- **Average Response Time**: 1-2 seconds
- **Max Response Time**: 5 seconds
- **Concurrent Users**: Up to 100
- **Availability**: 99.9% uptime

---

## Support

For API issues:
- Check `/health` endpoint
- Review logs: `gcloud run services logs read support-chatbot-api`
- Contact: dev@kalpana-ai.com

---

## Changelog

### v1.0.0 (2025-01-01)
- Initial release
- Gemini 2.5 Flash integration
- Multilingual support
- Quick help feature
- Session management
- Comprehensive knowledge base
