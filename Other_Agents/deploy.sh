#!/bin/bash

# Muse Agent Deployment Script
# Deploys the Muse Agent API to Google Cloud Run

set -e

echo "🚀 Deploying Muse Agent to Cloud Run..."

# Configuration
PROJECT_ID="nodal-fountain-470717-j1"
SERVICE_NAME="muse-agent-api"
REGION="us-central1"
BUCKET_NAME="kalpana-ai-craft-images"

# Set project
gcloud config set project $PROJECT_ID

# Check if bucket exists, create if not
echo "📦 Checking GCS bucket..."
if ! gsutil ls -b gs://$BUCKET_NAME 2>/dev/null; then
    echo "Creating bucket $BUCKET_NAME..."
    gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME
    echo "✅ Bucket created"
else
    echo "✅ Bucket already exists"
fi

# Make bucket public (for generated images)
echo "🔓 Setting bucket to public access..."
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME

# Build and deploy using Cloud Build
echo "🏗️  Building Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
echo "🚢 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 4Gi \
    --cpu 2 \
    --timeout 600 \
    --min-instances 0 \
    --max-instances 10 \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo ""
echo "✅ Deployment complete!"
echo "🌐 Service URL: $SERVICE_URL"
echo ""
echo "Test endpoints:"
echo "  Health: $SERVICE_URL/health"
echo "  Docs: $SERVICE_URL/docs"
echo "  Generate: POST $SERVICE_URL/generate"
echo ""
