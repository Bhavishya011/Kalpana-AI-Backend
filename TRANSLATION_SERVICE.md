# Translation Service - Separate from Main Product API

## Overview
The Translation Service is a **standalone microservice** completely separate from the main KalpanaAI product pipeline (`main2.0.py`). This ensures translation functionality doesn't interfere with product generation workflows.

## Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (Next.js)              │
│  - Components with useTranslation hooks │
└────────────┬────────────────────────────┘
             │
             ├─ /api/translate (Next.js API Route)
             │
             ↓
┌─────────────────────────────────────────┐
│   Translation Service (Port 8081)       │
│   - Separate Cloud Run service          │
│   - Uses Gemini AI for translation      │
│   - Independent from product pipeline   │
└─────────────────────────────────────────┘

                     vs

┌─────────────────────────────────────────┐
│   Main Product API (Port 8080)          │
│   - Storytelling pipeline                │
│   - Image generation                     │
│   - Pricing calculator                   │
│   - Market intelligence                  │
└─────────────────────────────────────────┘
```

## Files

### Backend (Translation Service)
- **`api/translation_service.py`** - Standalone FastAPI service
  - Port: 8081 (different from main API's 8080)
  - Endpoints: `/translate`, `/health`
  - Uses Gemini 2.0 Flash for AI translation

### Deployment
- **`Dockerfile.translation`** - Separate Docker container
- **`deploy-translation-service.sh`** - Bash deployment script
- **`deploy-translation-service.ps1`** - PowerShell deployment script

### Frontend
- **`src/lib/i18n/translate.ts`** - Translation client functions
- **`src/hooks/use-translation.ts`** - React hooks for auto-translation
- **`src/app/api/translate/route.ts`** - Next.js API proxy

## Deployment

### Option 1: PowerShell (Windows)
```powershell
.\deploy-translation-service.ps1
```

### Option 2: Bash (Mac/Linux)
```bash
chmod +x deploy-translation-service.sh
./deploy-translation-service.sh
```

### Manual Deployment
```bash
# Build
gcloud builds submit \
  --tag gcr.io/nodal-fountain-470717-j1/kalpana-translation \
  --dockerfile Dockerfile.translation

# Deploy
gcloud run deploy kalpana-translation \
  --image gcr.io/nodal-fountain-470717-j1/kalpana-translation \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8081
```

## API Endpoints

### POST /translate
Translate text, arrays, or entire objects.

**Request:**
```json
{
  "text": "Hello, artisan!",
  "targetLocale": "hi-IN",
  "sourceLocale": "en-US"
}
```

**Response:**
```json
{
  "translation": "नमस्ते, कारीगर!",
  "source_language": "English",
  "target_language": "Hindi",
  "success": true
}
```

**Batch Translation:**
```json
{
  "texts": ["Hello", "Welcome", "Thank you"],
  "targetLocale": "hi-IN"
}
```

**Object Translation:**
```json
{
  "object": {
    "title": "Beautiful Pottery",
    "description": "Handcrafted with love"
  },
  "targetLocale": "hi-IN"
}
```

### GET /health
Check service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "translation",
  "gemini": "connected",
  "supported_languages": {
    "en-US": "English",
    "hi-IN": "Hindi",
    ...
  }
}
```

## Frontend Usage

### 1. Translate Text in Components
```typescript
import { useTranslatedText } from '@/hooks/use-translation';

function MyComponent({ language }) {
  const text = "Your product is ready!";
  const translated = useTranslatedText(text, language);
  
  return <p>{translated}</p>;
}
```

### 2. Translate API Responses
```typescript
import { useTranslatedObject } from '@/hooks/use-translation';

function ProductDisplay({ apiResponse, language }) {
  const { data: translated, isTranslating } = useTranslatedObject(
    apiResponse,
    language
  );
  
  if (isTranslating) return <LoadingSpinner />;
  
  return (
    <div>
      <h1>{translated.title}</h1>
      <p>{translated.description}</p>
    </div>
  );
}
```

### 3. Manual Translation
```typescript
import { translateText, translateObject } from '@/lib/i18n/translate';

// Single text
const hindi = await translateText("Hello", "hi-IN");

// Object
const translated = await translateObject({
  title: "Pottery",
  price: "₹500"
}, "hi-IN");
```

## Key Features

### ✅ Separation of Concerns
- Translation service runs independently
- Doesn't affect product generation pipeline
- Can be scaled separately

### ✅ AI-Powered Translation
- Uses Gemini 2.0 Flash for natural translations
- Preserves formatting (emojis, ₹, line breaks)
- Context-aware for craft terminology
- Doesn't translate brand names (KalpanaAI, etc.)

### ✅ Batch Processing
- Translates multiple strings in one API call
- Efficient for translating entire objects
- Reduces API overhead

### ✅ Error Handling
- Fallback to original text on errors
- Graceful degradation
- No impact on user experience if service is down

## Environment Variables

### Backend (Translation Service)
```bash
GOOGLE_CLOUD_PROJECT=nodal-fountain-470717-j1
PORT=8081
```

### Frontend (Next.js)
```bash
TRANSLATION_API_URL=https://kalpana-translation-508329185712.us-central1.run.app
```

## Supported Languages

- 🇬🇧 English (en-US)
- 🇮🇳 Hindi (hi-IN) - हिन्दी
- 🇮🇳 Bengali (bn-IN) - বাংলা
- 🇮🇳 Tamil (ta-IN) - தமிழ்
- 🇮🇳 Telugu (te-IN) - తెలుగు
- 🇮🇳 Marathi (mr-IN) - मराठी
- 🇮🇳 Gujarati (gu-IN) - ગુજરાતી
- 🇮🇳 Kannada (kn-IN) - ಕನ್ನಡ

## Testing

### Test Translation Service
```bash
# Health check
curl https://kalpana-translation-508329185712.us-central1.run.app/health

# Translate text
curl -X POST https://kalpana-translation-508329185712.us-central1.run.app/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Beautiful handcrafted pottery from Jaipur",
    "targetLocale": "hi-IN"
  }'
```

### Test Frontend Integration
1. Change language in UI dropdown
2. Navigate to Add Product page
3. Generate a marketing kit
4. Verify all content is translated (title, description, pricing, etc.)

## Cost Optimization

- **Separate scaling**: Translation service uses less resources (1Gi vs 2Gi)
- **Min instances**: 0 (scales to zero when not in use)
- **Batch translation**: Reduces API calls
- **Caching**: Browser caches translations

## Troubleshooting

### Service Not Responding
```bash
# Check service status
gcloud run services describe kalpana-translation \
  --region us-central1 \
  --format yaml

# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=kalpana-translation" \
  --limit 50 \
  --format json
```

### Translation Quality Issues
- Adjust `temperature` in `translation_service.py` (currently 0.1)
- Modify translation prompt for better context
- Add domain-specific terminology to prompt

### Frontend Not Translating
1. Check browser console for errors
2. Verify `TRANSLATION_API_URL` is set correctly
3. Check if language prop is passed to components
4. Ensure `useTranslatedObject` hook is used for API responses

## Comparison: Main API vs Translation Service

| Feature | Main API (8080) | Translation Service (8081) |
|---------|-----------------|----------------------------|
| Purpose | Product pipeline | Translation only |
| Memory | 2Gi | 1Gi |
| CPU | 2 | 1 |
| Timeout | 300s | 60s |
| Min Instances | 1 | 0 |
| Max Instances | 10 | 5 |
| Dependencies | All agents, Firestore | Only Gemini AI |

## Next Steps

1. ✅ Deploy translation service: `.\deploy-translation-service.ps1`
2. ✅ Test translation API
3. ✅ Update frontend components with translation hooks
4. 🔄 Monitor usage and costs
5. 🔄 Add caching layer if needed

## Support

For issues or questions:
- Check logs: `gcloud logging read ...`
- Review documentation: `MULTILINGUAL_SYSTEM.md`
- Test endpoints manually with curl
