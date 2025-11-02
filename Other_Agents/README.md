# Muse Agent API

AI-powered craft variation generator that creates 4 unique interpretations from a single craft image.

## Features

- **Input:** 1 craft image (JPG, PNG)
- **Output:** 4 generated variations
  - 2 traditional variations (same style, different colors)
  - 2 modern implementations (contemporary applications)
- **Powered by:** Google Vertex AI (Gemini 2.0 Flash + Imagen 4.0)
- **Deployed on:** Google Cloud Run

## API Endpoints

### Health Check
```bash
GET /health
```

### Generate Variations
```bash
POST /generate
Content-Type: multipart/form-data

Body:
- image: craft image file
```

### API Documentation
```bash
GET /docs
```

## Deployment

### Prerequisites
- Google Cloud SDK installed
- Authenticated with `gcloud auth login`
- Project: `nodal-fountain-470717-j1`

### Deploy to Cloud Run

**Windows (PowerShell):**
```powershell
cd Other_Agents
.\deploy.ps1
```

**Linux/Mac:**
```bash
cd Other_Agents
chmod +x deploy.sh
./deploy.sh
```

## Testing

```bash
python test_muse_api.py <API_URL>
```

Example:
```bash
python test_muse_api.py https://muse-agent-api-508329185712.us-central1.run.app
```

## Usage Example

```python
import requests

# Upload craft image
files = {'image': open('craft_image.jpg', 'rb')}
response = requests.post(
    'https://muse-agent-api-508329185712.us-central1.run.app/generate',
    files=files,
    timeout=180
)

result = response.json()

# Get generated images
traditional_images = result['data']['traditional_images']
modern_images = result['data']['modern_images']

print(f"Generated {len(traditional_images)} traditional variations")
print(f"Generated {len(modern_images)} modern implementations")
```

## Architecture

```
Input Image 
    ↓
Upload to GCS
    ↓
Gemini Analysis → Extract craft details
    ↓
Research Techniques → Artisan feasibility
    ↓
Generate Ideas → 2 traditional + 2 modern
    ↓
Create Prompts → Detailed image prompts
    ↓
Imagen Generation → 4 images (with fallback)
    ↓
Save to GCS → Public URLs
    ↓
Return Response
```

## Environment Variables

- `GOOGLE_CLOUD_PROJECT`: GCP project ID (auto-set by Cloud Run)
- `PORT`: Server port (auto-set by Cloud Run, default: 8080)

## Resource Requirements

- **Memory:** 4GB
- **CPU:** 2 vCPU
- **Timeout:** 10 minutes
- **Concurrency:** 10 max instances

## GCS Bucket

All generated images are stored in:
```
gs://kalpana-ai-craft-images/
```

Organized by session:
```
craft_gen_YYYYMMDD_HHMMSS_<uuid>/
  ├── traditional_1.png
  ├── traditional_2.png
  ├── modern_1.png
  └── modern_2.png
```

## Error Handling

- **400:** Invalid file type
- **500:** Generation error (check logs)
- **Timeout:** First request may timeout (cold start), retry after 30s

## Monitoring

View logs:
```bash
gcloud run services logs read muse-agent-api --region=us-central1
```

## Cost Estimate

- **Cloud Run:** ~$0.10 per 1000 requests
- **Imagen 4.0:** ~$0.02 per image
- **GCS Storage:** ~$0.02/GB/month
- **Total per request:** ~$0.10 (4 images + processing)

## Support

For issues or questions, contact the Kalpana AI team.
