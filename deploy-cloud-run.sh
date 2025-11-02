#!/bin/bash
set -e

# Configuration
PROJECT_ID="nodal-fountain-470717-j1"
REGION="us-central1"
SERVICE_NAME="kalpana-ai-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying KalpanaAI to Google Cloud Run..."
echo "================================================"
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"
echo "================================================"

# Set the project
echo "📋 Setting Google Cloud project..."
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudscheduler.googleapis.com \
    cloudbuild.googleapis.com \
    firestore.googleapis.com \
    aiplatform.googleapis.com \
    storage.googleapis.com

# Build the container image
echo "🏗️  Building Docker image..."
cd "$(dirname "$0")"  # Go to script directory
gcloud builds submit --tag ${IMAGE_NAME} --config=cloudbuild.yaml .

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 1 \
    --port 8080 \
    --set-env-vars GOOGLE_CLOUD_PROJECT=${PROJECT_ID} \
    --set-env-vars PORT=8080

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

echo "✅ Cloud Run deployment complete!"
echo "🌐 Service URL: ${SERVICE_URL}"

# Create Cloud Scheduler job for weekly market updates
echo ""
echo "⏰ Setting up Cloud Scheduler for automatic market updates..."

# Create scheduler job (if it doesn't exist)
gcloud scheduler jobs create http market-trends-update \
    --location ${REGION} \
    --schedule "0 2 * * 0" \
    --time-zone "Asia/Kolkata" \
    --uri "${SERVICE_URL}/api/update-market-trends" \
    --http-method POST \
    --oidc-service-account-email "${PROJECT_ID}@appspot.gserviceaccount.com" \
    --description "Weekly market trends update from Google Trends" \
    --attempt-deadline 600s \
    2>/dev/null || echo "⚠️  Scheduler job already exists, updating..."

# Update if already exists
gcloud scheduler jobs update http market-trends-update \
    --location ${REGION} \
    --schedule "0 2 * * 0" \
    --time-zone "Asia/Kolkata" \
    --uri "${SERVICE_URL}/api/update-market-trends" \
    --http-method POST \
    --oidc-service-account-email "${PROJECT_ID}@appspot.gserviceaccount.com" \
    --description "Weekly market trends update from Google Trends" \
    --attempt-deadline 600s \
    2>/dev/null || true

echo "✅ Cloud Scheduler configured!"

# Run initial market update
echo ""
echo "📈 Running initial market trends update..."
curl -X POST "${SERVICE_URL}/api/update-market-trends" || echo "⚠️  Initial update will run on first request"

echo ""
echo "================================================"
echo "✅ Deployment Complete!"
echo "================================================"
echo "🌐 API URL: ${SERVICE_URL}"
echo "📊 Health Check: ${SERVICE_URL}/api/health"
echo "📈 Market Trends: ${SERVICE_URL}/api/market-trends"
echo "⏰ Auto-update: Every Sunday 2:00 AM IST"
echo ""
echo "🧪 Test your API:"
echo "curl ${SERVICE_URL}/api/health"
echo ""
echo "📋 View logs:"
echo "gcloud run logs read ${SERVICE_NAME} --region ${REGION} --limit 50"
echo ""
echo "🔄 To manually trigger market update:"
echo "curl -X POST ${SERVICE_URL}/api/update-market-trends"
echo "================================================"
