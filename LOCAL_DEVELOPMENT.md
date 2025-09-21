# Local Development Environment

This setup allows you to run the KalpanaAI API locally and integrate it with your frontend.

## Quick Start

### 1. Start Local API Server
```bash
cd api
python local_main.py
```

The API will run on `http://localhost:8080`

### 2. Update Frontend Configuration

Update your frontend proxy in `src/app/api/proxy/route.ts` to point to local:

```typescript
const KALPANA_API_URL = "http://localhost:8080";  // Local development
// const KALPANA_API_URL = "https://kalpanaai-storytelling-418149026163.us-central1.run.app";  // Production
```

### 3. Start Frontend
```bash
cd Kalpana-AI
npm run dev
```

## API Response Structure

The local API now returns exactly what your frontend expects:

```typescript
{
  marketing_kit: {
    productPosts: [
      {
        image_url: string | null,
        description: string
      }
    ],
    storyPosts: [
      {
        image_url: string | null,
        story: string,
        caption: string
      }
    ]
  }
}
```

## Development Features

- ✅ CORS configured for localhost:3000
- ✅ Response structure matches TypeScript interfaces
- ✅ Form data handling for file uploads
- ✅ Real story generation when enable_generation=true
- ✅ Graceful fallback to placeholder content
- ✅ Static file serving for generated assets

## Testing

Test the local API directly:
```bash
curl -X POST "http://localhost:8080/api/storytelling/generate" \
  -F "description=handwoven silk scarf" \
  -F "enable_generation=true"
```

## File Structure

```
api/
├── local_main.py       # Local development server
├── main.py            # Original Cloud Run version
└── generated_assets/  # Static files for images (auto-created)
```