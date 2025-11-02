# 🚀 Quick Start: Deploy to Google Cloud Run

## Prerequisites ✅

1. **Google Cloud SDK** installed
   - Download: https://cloud.google.com/sdk/docs/install
   - Verify: `gcloud --version`

2. **Authenticated with Google Cloud**
   ```bash
   gcloud auth login
   gcloud config set project nodal-fountain-470717-j1
   ```

3. **Billing enabled** on project `nodal-fountain-470717-j1` ✅

---

## One-Command Deployment 🎯

### Windows
```cmd
deploy-cloud-run.bat
```

### Linux/Mac
```bash
chmod +x deploy-cloud-run.sh
./deploy-cloud-run.sh
```

---

## What Gets Deployed?

### 1. **Cloud Run Service** 🏃
- **Name**: `kalpana-ai-api`
- **Region**: `us-central1`
- **URL**: `https://kalpana-ai-api-xxxx.run.app`
- **Specs**: 2 CPU, 2 GiB RAM, 1-10 instances

### 2. **Cloud Scheduler** ⏰
- **Job**: `market-trends-update`
- **Schedule**: Every Sunday 2:00 AM IST
- **Action**: Calls `/api/update-market-trends`
- **Purpose**: Auto-update Google Trends data weekly

---

## Deployment Process

The script will:
1. ✅ Enable required Google Cloud APIs
2. 🏗️ Build Docker container with Cloud Build
3. 🚀 Deploy to Cloud Run
4. ⏰ Set up Cloud Scheduler for weekly updates
5. 📈 Run initial market trends update
6. 🌐 Display your API URL

**⏱️ Total Time**: ~5-10 minutes

---

## After Deployment

### 1. Get Your Service URL
```bash
gcloud run services describe kalpana-ai-api \
    --region us-central1 \
    --format 'value(status.url)'
```

### 2. Test Health Endpoint
```bash
curl https://your-service-url.run.app/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "2.0-with-pricing-and-market-intelligence",
  "agents": {
    "storyteller": "available",
    "image_generator": "available",
    "synthesizer": "available",
    "curator": "available",
    "pricing": "available",
    "market_intelligence": "available"
  },
  "market_cache": {
    "status": "available",
    "last_updated": "2025-10-26T15:43:45.476433",
    "age_days": 0,
    "needs_update": false,
    "categories": 8,
    "trending_crafts": 2
  },
  "services": {
    "firestore": "connected",
    "vertex_ai": "connected",
    "google_trends": "connected"
  }
}
```

### 3. Test Market Trends Endpoint
```bash
curl https://your-service-url.run.app/api/market-trends
```

### 4. Manual Market Update (if needed)
```bash
curl -X POST https://your-service-url.run.app/api/update-market-trends
```

---

## Update Your Frontend

Update your Next.js app to use the Cloud Run URL:

**File**: `Kalpana-AI/src/app/add-product/page.tsx`

```typescript
// Change this:
const API_URL = 'http://localhost:8000';

// To this (replace with your actual Cloud Run URL):
const API_URL = 'https://kalpana-ai-api-xxxx.run.app';
```

---

## Monitoring & Logs

### View Logs
```bash
# Real-time logs
gcloud run logs tail kalpana-ai-api --region us-central1

# Last 50 logs
gcloud run logs read kalpana-ai-api --region us-central1 --limit 50

# Filter for market updates
gcloud run logs read kalpana-ai-api --region us-central1 | grep "market"
```

### Cloud Console
- **Service**: https://console.cloud.google.com/run
- **Logs**: https://console.cloud.google.com/logs
- **Scheduler**: https://console.cloud.google.com/cloudscheduler
- **Metrics**: https://console.cloud.google.com/monitoring

---

## Troubleshooting

### Issue: Build Fails
```bash
# Check Cloud Build logs
gcloud builds list --limit 5

# View specific build
gcloud builds log BUILD_ID
```

### Issue: Service Won't Start
```bash
# Check service logs
gcloud run logs read kalpana-ai-api --region us-central1 --limit 100

# Check service status
gcloud run services describe kalpana-ai-api --region us-central1
```

### Issue: Scheduler Not Running
```bash
# Check scheduler job
gcloud scheduler jobs describe market-trends-update --location us-central1

# Run manually
gcloud scheduler jobs run market-trends-update --location us-central1

# Check scheduler logs
gcloud logging read "resource.type=cloud_scheduler_job AND resource.labels.job_id=market-trends-update" --limit 10
```

### Issue: Out of Memory
```bash
# Increase memory to 4 GiB
gcloud run services update kalpana-ai-api \
    --region us-central1 \
    --memory 4Gi
```

---

## Updating Your Deployment

### Deploy New Version
```bash
# Just run the deployment script again
./deploy-cloud-run.sh

# Or manual update
cd api
gcloud builds submit --tag gcr.io/nodal-fountain-470717-j1/kalpana-ai-api .
gcloud run services update kalpana-ai-api \
    --image gcr.io/nodal-fountain-470717-j1/kalpana-ai-api \
    --region us-central1
```

### Rollback to Previous Version
```bash
# List revisions
gcloud run revisions list --service kalpana-ai-api --region us-central1

# Rollback
gcloud run services update-traffic kalpana-ai-api \
    --region us-central1 \
    --to-revisions REVISION_NAME=100
```

---

## Cost Estimate 💰

### Monthly Costs (Estimated)
- **Cloud Run**: $10-20/month (with min 1 instance)
- **Cloud Build**: $0-5/month (free tier covers most builds)
- **Cloud Scheduler**: $0.10/job/month
- **Vertex AI API**: Pay-per-use (free tier available)
- **Firestore**: Pay-per-use (free tier covers small usage)

**Total**: ~$15-30/month depending on traffic

### Cost Optimization
```bash
# Remove min instance (adds cold starts)
gcloud run services update kalpana-ai-api \
    --region us-central1 \
    --min-instances 0

# Reduce memory
gcloud run services update kalpana-ai-api \
    --region us-central1 \
    --memory 1Gi
```

---

## Next Steps

1. ✅ Deploy to Cloud Run
2. ✅ Verify health endpoint
3. ✅ Test market trends endpoint
4. ✅ Update frontend with Cloud Run URL
5. ✅ Test complete flow (create product with pricing)
6. 📱 Deploy frontend to Vercel/Netlify
7. 🎨 Add custom domain (optional)
8. 🔐 Add authentication (optional)
9. 📊 Set up monitoring alerts (optional)

---

## Support

### Documentation
- [Cloud Run Docs](https://cloud.google.com/run/docs)
- [Cloud Scheduler Docs](https://cloud.google.com/scheduler/docs)
- [Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)

### Getting Help
- Check logs first: `gcloud run logs read kalpana-ai-api --region us-central1`
- Check health endpoint: `/api/health`
- Review error messages in console
- Common issues documented in CLOUD_RUN_DEPLOYMENT.md

---

## Success! 🎉

Your KalpanaAI API is now:
- ✅ Running on Google Cloud Run
- ✅ Auto-scaling from 1-10 instances
- ✅ Auto-updating market trends weekly
- ✅ Using Gemini AI for complexity analysis
- ✅ Using Google Trends for market intelligence
- ✅ Ready for production traffic!

**Your API**: `https://kalpana-ai-api-xxxx.run.app`
