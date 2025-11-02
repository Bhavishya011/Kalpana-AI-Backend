# Cloud Run Service Configuration

## Service Details
- **Service Name**: kalpana-ai-api
- **Project**: nodal-fountain-470717-j1
- **Region**: us-central1
- **Platform**: Cloud Run (fully managed)

## Resources
- **Memory**: 2 GiB
- **CPU**: 2
- **Timeout**: 300 seconds (5 minutes)
- **Max Instances**: 10
- **Min Instances**: 1 (always warm)
- **Port**: 8080

## Environment Variables
- `GOOGLE_CLOUD_PROJECT`: nodal-fountain-470717-j1
- `PORT`: 8080

## Auto-Scaling
- Scales from 1 to 10 instances based on traffic
- Min 1 instance ensures no cold starts
- Each instance handles multiple concurrent requests

## Cloud Scheduler Integration
- **Job Name**: market-trends-update
- **Schedule**: `0 2 * * 0` (Every Sunday at 2:00 AM IST)
- **Endpoint**: `/api/update-market-trends`
- **Method**: POST
- **Timeout**: 600 seconds (10 minutes)
- **Authentication**: OIDC Service Account

## Deployment

### Prerequisites
1. Google Cloud SDK installed
2. Docker installed (for local testing)
3. Authenticated with gcloud: `gcloud auth login`
4. Project set: `gcloud config set project nodal-fountain-470717-j1`

### Deploy to Cloud Run
```bash
# Windows
.\deploy-cloud-run.bat

# Linux/Mac
chmod +x deploy-cloud-run.sh
./deploy-cloud-run.sh
```

### Manual Deployment Steps
```bash
# 1. Build container image
cd api
gcloud builds submit --tag gcr.io/nodal-fountain-470717-j1/kalpana-ai-api .

# 2. Deploy to Cloud Run
gcloud run deploy kalpana-ai-api \
    --image gcr.io/nodal-fountain-470717-j1/kalpana-ai-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 1 \
    --port 8080 \
    --set-env-vars GOOGLE_CLOUD_PROJECT=nodal-fountain-470717-j1,PORT=8080

# 3. Create Cloud Scheduler job
gcloud scheduler jobs create http market-trends-update \
    --location us-central1 \
    --schedule "0 2 * * 0" \
    --time-zone "Asia/Kolkata" \
    --uri "https://kalpana-ai-api-xxxx.run.app/api/update-market-trends" \
    --http-method POST \
    --oidc-service-account-email "nodal-fountain-470717-j1@appspot.gserviceaccount.com"
```

## Testing

### Health Check
```bash
curl https://your-service-url.run.app/api/health
```

### Manual Market Update
```bash
curl -X POST https://your-service-url.run.app/api/update-market-trends
```

### View Logs
```bash
gcloud run logs read kalpana-ai-api --region us-central1 --limit 50
```

### Test Locally
```bash
# Build Docker image
docker build -t kalpana-ai-api .

# Run locally
docker run -p 8080:8080 \
    -e GOOGLE_CLOUD_PROJECT=nodal-fountain-470717-j1 \
    -e PORT=8080 \
    kalpana-ai-api

# Test
curl http://localhost:8080/api/health
```

## Monitoring

### Cloud Console
- **Service Dashboard**: https://console.cloud.google.com/run/detail/us-central1/kalpana-ai-api
- **Logs**: https://console.cloud.google.com/logs
- **Scheduler**: https://console.cloud.google.com/cloudscheduler

### Metrics to Monitor
- Request count and latency
- Instance count (scaling behavior)
- Error rate
- Market update success rate
- Cache freshness (via health endpoint)

## Cost Optimization

### Current Configuration Costs (Estimated)
- **Always-on (min 1 instance)**: ~$10-15/month
- **API calls**: Pay per request after free tier
- **Cloud Scheduler**: $0.10/job/month
- **Cloud Build**: Free tier covers most builds

### To Reduce Costs
1. Set `--min-instances 0` (but adds cold start latency)
2. Reduce memory to 1Gi if sufficient
3. Reduce CPU to 1 if performance acceptable

## Security

### Current Setup
- ✅ HTTPS enforced
- ✅ CORS configured for frontend
- ✅ Service account authentication for scheduler
- ⚠️  Public access allowed (--allow-unauthenticated)

### To Secure Further
1. Add API key authentication
2. Restrict CORS to specific origins
3. Use Cloud IAP for admin endpoints
4. Add rate limiting

## Troubleshooting

### Container Won't Start
```bash
# Check logs
gcloud run logs read kalpana-ai-api --region us-central1 --limit 100

# Common issues:
# - Missing dependencies in requirements.txt
# - Wrong working directory in Dockerfile
# - Port not matching PORT env var
```

### Scheduler Not Working
```bash
# Check scheduler logs
gcloud scheduler jobs describe market-trends-update --location us-central1

# Run manually
gcloud scheduler jobs run market-trends-update --location us-central1
```

### Out of Memory
```bash
# Increase memory
gcloud run services update kalpana-ai-api \
    --region us-central1 \
    --memory 4Gi
```

## Rollback

### To Previous Version
```bash
# List revisions
gcloud run revisions list --service kalpana-ai-api --region us-central1

# Rollback
gcloud run services update-traffic kalpana-ai-api \
    --region us-central1 \
    --to-revisions REVISION_NAME=100
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: nodal-fountain-470717-j1
      
      - name: Build and Deploy
        run: |
          gcloud builds submit --tag gcr.io/nodal-fountain-470717-j1/kalpana-ai-api ./api
          gcloud run deploy kalpana-ai-api \
            --image gcr.io/nodal-fountain-470717-j1/kalpana-ai-api \
            --region us-central1 \
            --platform managed
```
