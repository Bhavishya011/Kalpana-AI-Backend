# KalpanaAI Backend

## Google Cloud-Native AI Agent System for Artisan Empowerment

KalpanaAI Backend is an AI-powered storytelling and image enhancement platform designed for artisans. It combines specialized Python agents to produce compelling marketing assets, improve product photography, and generate culturally grounded narratives for commerce.

## API Endpoint

`https://artisan-mentor-api-508329185712.us-central1.run.app`

Fully operational deployment endpoint for the hosted API.

## Agent Architecture

KalpanaAI backend runs specialized AI agents that are modular, independently testable, and cloud-deployable.

| Agent | Function | Services |
| --- | --- | --- |
| Orchestrator | Workflow coordination and fault handling | FastAPI, Cloud Run |
| Curator | Product photo enhancement | Vision API, Imagen |
| Storyteller | Culturally grounded storytelling | Gemini, Firestore RAG |
| Image Generator | Story visual creation | Imagen |
| Dynamic Price | Fair pricing recommendations | Market intelligence data |
| Synthesizer | Final marketing kit assembly | Storage pipeline |
| Craft DNA | Heritage proof and QR generation | Firestore, Storage |
| Market Intelligence | Trend detection and enrichment | Trends API cache |

## Key Innovations

### Cultural RAG Guardrails

- Firestore-backed cultural knowledge retrieval
- Heritage-aware prompt design and output checks
- Confidence-driven review patterns for sensitive cultural outputs

### Agentic Commerce Workflow

- Multi-agent generation pipeline from one product input
- Story, images, and pricing assembled as a single marketing kit
- Designed for AP2-style autonomous commerce readiness

### Rural-Optimized Product Flow

- Lightweight payload paths for constrained networks
- Voice and image-first inputs for creator usability
- Compatibility with multilingual frontend experiences

## API Endpoints

Main API file: `api/main2.0.py`

- `GET /`
- `GET /favicon.ico`
- `GET /health`
- `POST /test-curator`
- `POST /test-curator-full`
- `POST /api/storytelling/generate`
- `POST /api/update-market-trends`
- `GET /api/market-trends`
- `POST /api/translate-text`
- `POST /api/craft-dna/generate`
- `GET /heritage/{heritage_id}`

OpenAPI references in this workspace:

- `openapi_schema.json`
- `Kalpana-AI/openapi_spec.json`

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Runtime | Python 3.11, Docker |
| API | FastAPI, Uvicorn |
| AI/ML | Vertex AI (Gemini, Imagen), Vision API |
| Data | Firestore, cached market intelligence |
| Storage | Local and Cloud Storage-compatible asset flow |
| Auth | Google Cloud ADC / IAM |
| Deployment | Google Cloud Run, App Engine |
| Monitoring | Cloud Logging-compatible structured logs |

## Project Structure

```text
.
|- Agents/
|  |- agents/
|  |  |- curator_agent.py
|  |  |- image_generator_agent.py
|  |  |- storyteller_agent.py
|  |  |- synthesizer_agent.py
|  |  |- orchestrator.py
|  |  |- pricing_agent.py
|  |  |- market_intelligence.py
|  |  |- craft_dna_agent.py
|  |- storytelling_kit/
|  |- test_*.py
|- api/
|  |- main2.0.py
|  |- startup_main.py
|  |- translation_service.py
|  |- requirements.txt
|- app.py
|- app.yaml
|- Dockerfile
|- requirements.txt
|- README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud project with billing enabled
- Vertex AI and Vision APIs enabled
- Firestore configured

### Environment Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
```

### Required Environment Variables

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

### Run the Server

Recommended:

```bash
python api/main2.0.py
```

Alternative dev server:

```bash
cd api
uvicorn main2.0:app --reload --host 0.0.0.0 --port 8000
```

Local URLs:

- `http://localhost:8000`
- `http://localhost:8000/docs`
- `http://localhost:8000/health`
- `http://localhost:8000/test-curator`

## Request and Response Example

`POST /api/storytelling/generate` accepts multipart form data.

Typical request fields:

- `description` (required)
- `photo` (optional file)
- `material_cost` (optional)

Example request:

```bash
curl -X POST "http://localhost:8000/api/storytelling/generate" \
  -F "description=Traditional Kutch pottery vase" \
  -F "material_cost=150" \
  -F "photo=@./sample.jpg"
```

Typical response shape:

```json
{
  "status": "success",
  "asset_id": "uuid-asset-identifier",
  "marketing_kit": {
    "story_title": "Generated story title",
    "story_text": "Complete narrative",
    "assets": {
      "story_images": ["url1", "url2"],
      "enhanced_photos": ["enhanced_url1", "enhanced_url2"]
    }
  }
}
```

## Deployment

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

Deployment helper scripts:

- `deploy-cloud-run.sh`
- `deploy-cloud-run.bat`
- `deploy_backend.ps1`

## Testing

Agent-level tests:

```bash
python Agents/test_storyteller_minimal.py
python Agents/test_story_image_generation.py
python Agents/test_curator_imagen4.py
```

Full pipeline test:

```bash
python Agents/run_storytelling_pipeline.py
```

## Monitoring and Observability

- `/health` for API and agent-level health checks
- Structured logs for request and pipeline tracing
- Error details captured in endpoint responses and server logs

## Troubleshooting

- `403`: Billing, IAM permissions, or API enablement issue
- `429`: Quota/rate limit reached
- `500`: Agent initialization or runtime failure
- Translation issues: verify translation service deployment and URL configuration

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Add or update tests for your changes.
4. Submit a pull request with clear verification notes.

## License

MIT License. See `LICENSE` for details.

## Contact and Resources

- Project Lead: Bhavishya Jain
- Frontend Repo: `https://github.com/Bhavishya011/Kalpana-AI`
- Live Demo: `https://kalpana-ai.vercel.app`
- Hackathon: Google Cloud Gen AI Exchange 2025

KalpanaAI Backend mission: preserve endangered crafts, expand artisan reach, and build ethical AI systems for cultural commerce.
