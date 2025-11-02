# 🏗️ KalpanaAI Architecture - Cloud Run Deployment

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER / FRONTEND                          │
│                     (Next.js on Vercel)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GOOGLE CLOUD RUN                             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  KalpanaAI API                            │  │
│  │               (FastAPI Container)                         │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │         Main Endpoints                           │     │  │
│  │  │  • POST /api/generate-storytelling              │     │  │
│  │  │  • GET  /api/market-trends                      │     │  │
│  │  │  • POST /api/update-market-trends               │     │  │
│  │  │  • GET  /api/health                             │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │         Agent Pipeline                           │     │  │
│  │  │                                                   │     │  │
│  │  │  1. CuratorAgent          (Heritage Data)       │     │  │
│  │  │  2. StorytellerAgent       (AI Story)           │     │  │
│  │  │  3. ImageGeneratorAgent    (AI Images)          │     │  │
│  │  │  4. SynthesizerAgent       (Marketing Kit)      │     │  │
│  │  │  5. DynamicPricingAgent    (Smart Pricing)      │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │      Market Intelligence Module                  │     │  │
│  │  │  • Google Trends API integration                │     │  │
│  │  │  • 8 craft categories tracking                  │     │  │
│  │  │  • Regional trends (Indian states)              │     │  │
│  │  │  • Seasonal trends (festivals)                  │     │  │
│  │  │  • market_cache.json (7-day expiry)             │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Resources: 2 CPU, 2 GiB RAM, 1-10 instances                   │
└────────────────┬───────────────────────────┬────────────────────┘
                 │                           │
                 │                           │
       ┌─────────▼─────────┐       ┌────────▼─────────┐
       │   Vertex AI       │       │   Firestore      │
       │                   │       │                  │
       │ • Gemini 2.0      │       │ • Heritage DB    │
       │ • Imagen 4        │       │ • Product Data   │
       │ • Complexity AI   │       │ • Artisan Info   │
       └───────────────────┘       └──────────────────┘
```

## Automated Market Updates

```
┌─────────────────────────────────────────────────────────────────┐
│                   CLOUD SCHEDULER                               │
│                                                                  │
│  Job: market-trends-update                                      │
│  Schedule: 0 2 * * 0 (Every Sunday 2 AM IST)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ POST /api/update-market-trends
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    KALPANAAI API                                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │     Market Intelligence Module                            │  │
│  │                                                            │  │
│  │  1. Fetch Google Trends for 8 categories                 │  │
│  │     (pottery, embroidery, jewelry, etc.)                 │  │
│  │                                                            │  │
│  │  2. Fetch regional trends for Indian states              │  │
│  │                                                            │  │
│  │  3. Fetch seasonal trends for festivals                  │  │
│  │                                                            │  │
│  │  4. Calculate trend scores (0-100)                       │  │
│  │                                                            │  │
│  │  5. Determine trend direction (rising/falling/stable)    │  │
│  │                                                            │  │
│  │  6. Adjust price ranges based on demand                  │  │
│  │                                                            │  │
│  │  7. Save to market_cache.json                            │  │
│  │     (Valid for 7 days)                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Google Trends   │
                    │ API             │
                    │ (pytrends)      │
                    └─────────────────┘
```

## Pricing Calculation Flow

```
User uploads product + material cost ($100)
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│              DYNAMIC PRICING AGENT                              │
│                                                                  │
│  1. Heritage Score (30% weight)                                 │
│     ├─ Query Firestore for artisan heritage data               │
│     └─ Score: 8/10 → Contribution: 2.4                          │
│                                                                  │
│  2. Complexity Score (40% weight)                               │
│     ├─ Analyze product description with Gemini AI              │
│     ├─ Detect 20+ traditional techniques                        │
│     └─ Score: 7/10 → Contribution: 2.8                          │
│                                                                  │
│  3. Market Demand (30% weight)                                  │
│     ├─ Read market_cache.json                                   │
│     ├─ Category: Embroidery (trending, score 71)               │
│     ├─ Trend multiplier: 1.15x                                  │
│     └─ Score: 8/10 → Contribution: 2.4                          │
│                                                                  │
│  Total Score: 7.6/10                                            │
│  Base Markup: 76% of material cost                              │
│  Trend Adjusted: 76% × 1.15 = 87.4%                            │
│                                                                  │
│  FINAL PRICE:                                                    │
│  Material: $100                                                  │
│  Markup:   $87.40                                                │
│  Total:    $187.40                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Flow

```
Developer runs: deploy-cloud-run.bat
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│  DEPLOYMENT STEPS                                               │
│                                                                  │
│  1. Enable Google Cloud APIs                                    │
│     ├─ Cloud Run                                                │
│     ├─ Cloud Scheduler                                          │
│     ├─ Cloud Build                                              │
│     ├─ Firestore                                                │
│     ├─ Vertex AI                                                │
│     └─ Cloud Storage                                            │
│                                                                  │
│  2. Build Docker Container                                      │
│     ├─ Copy Dockerfile + requirements.txt                       │
│     ├─ Copy API code (main2.0.py)                               │
│     ├─ Copy all agent modules                                   │
│     ├─ Install Python dependencies                              │
│     └─ Tag: gcr.io/nodal-fountain-470717-j1/kalpana-ai-api     │
│                                                                  │
│  3. Deploy to Cloud Run                                         │
│     ├─ Region: us-central1                                      │
│     ├─ CPU: 2 cores                                             │
│     ├─ Memory: 2 GiB                                            │
│     ├─ Min Instances: 1 (no cold starts)                        │
│     ├─ Max Instances: 10 (auto-scale)                           │
│     ├─ Timeout: 300 seconds                                     │
│     └─ Public access: Enabled                                   │
│                                                                  │
│  4. Create Cloud Scheduler Job                                  │
│     ├─ Name: market-trends-update                               │
│     ├─ Schedule: Every Sunday 2 AM IST                          │
│     ├─ Target: POST /api/update-market-trends                   │
│     ├─ Auth: OIDC Service Account                               │
│     └─ Timeout: 600 seconds                                     │
│                                                                  │
│  5. Initial Market Update                                       │
│     ├─ Call /api/update-market-trends                           │
│     ├─ Fetch Google Trends data                                 │
│     └─ Populate market_cache.json                               │
│                                                                  │
│  6. Success!                                                     │
│     └─ Service URL: https://kalpana-ai-api-xxxx.run.app        │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow - Create Product

```
Frontend (Next.js)
    │
    │ POST /api/generate-storytelling
    │ {
    │   photo: File,
    │   artist_name: "Rajesh Kumar",
    │   craft_type: "embroidery",
    │   material_cost: 100
    │ }
    │
    ▼
Cloud Run API
    │
    ├─► CuratorAgent
    │   │ • Analyze uploaded photo
    │   │ • Detect craft type
    │   │ • Extract colors, patterns
    │   │ • Query Firestore for heritage data
    │   └─► Heritage Score: 8/10
    │
    ├─► StorytellerAgent
    │   │ • Generate compelling product story
    │   │ • Use Gemini 2.0 Flash
    │   │ • Incorporate heritage context
    │   └─► Story: "Handcrafted with love..."
    │
    ├─► ImageGeneratorAgent
    │   │ • Generate 3 lifestyle images
    │   │ • Use Imagen 4
    │   │ • Show product in use cases
    │   └─► Images: [image1.jpg, image2.jpg, image3.jpg]
    │
    ├─► SynthesizerAgent
    │   │ • Create marketing kit JSON
    │   │ • Generate social media post
    │   │ • Format for e-commerce
    │   └─► Marketing kit ready
    │
    └─► DynamicPricingAgent
        │ • Calculate heritage score (30%)
        │ • Analyze complexity with AI (40%)
        │ • Check market trends (30%)
        │ • Read market_cache.json
        │ • Apply trend multipliers
        │ • Calculate final price
        └─► Price: ₹187 (material: ₹100 + markup: ₹87)
    
    │
    ▼
Response to Frontend
{
  "status": "success",
  "story": "...",
  "images": [...],
  "marketing_kit": {...},
  "pricing": {
    "base_price": 100,
    "markup": 87,
    "final_price": 187,
    "scores": {
      "heritage": 8,
      "complexity": 7,
      "market_demand": 8
    }
  }
}
```

## Key Features

### 1. **Auto-Scaling**
- Scales from 1 to 10 instances automatically
- Min 1 instance = no cold starts
- Handles traffic spikes gracefully

### 2. **Market Intelligence**
- Updates every Sunday automatically
- Tracks 8 craft categories
- Regional trends for Indian states
- Seasonal trends for festivals
- 7-day cache validity

### 3. **AI-Powered Pricing**
- Gemini AI for complexity analysis
- Google Trends for market demand
- Firestore for heritage data
- Dynamic multipliers (0.8x - 1.2x)

### 4. **Reliability**
- Health checks every 30 seconds
- Automatic restarts on failure
- Structured logging
- Error tracking

### 5. **Cost Optimization**
- Pay only for actual usage
- Auto-shutdown when idle (if min=0)
- Efficient container image
- Optimized dependencies

## Monitoring

### Health Check
- **Endpoint**: `/api/health`
- **Frequency**: Every 30 seconds
- **Checks**: All agents, market cache, API connections

### Logs
- **Real-time**: `gcloud run logs tail kalpana-ai-api`
- **Historical**: Cloud Logging console
- **Structured**: JSON format for easy parsing

### Metrics
- Request count & latency
- Error rate & types
- Instance count & CPU usage
- Memory usage & trends

## Security

### Current
- ✅ HTTPS enforced
- ✅ CORS configured
- ✅ Environment variables for secrets
- ✅ Service account for scheduler

### Recommended Additions
- 🔐 API key authentication
- 🔐 Rate limiting
- 🔐 Input validation & sanitization
- 🔐 Cloud IAP for admin endpoints

## Cost Breakdown

### Monthly Estimates
| Service | Usage | Cost |
|---------|-------|------|
| Cloud Run | 1 instance always + auto-scale | $10-20 |
| Cloud Scheduler | 1 job × 4 runs/month | $0.10 |
| Cloud Build | ~10 builds/month | $0-5 |
| Vertex AI (Gemini) | ~1000 requests | $5-15 |
| Firestore | Small dataset | $1-5 |
| **Total** | | **~$20-45/month** |

### Optimization Tips
1. Set `--min-instances 0` to save ~$10/month (adds cold starts)
2. Use caching to reduce AI API calls
3. Batch image generation requests
4. Monitor and optimize memory usage
