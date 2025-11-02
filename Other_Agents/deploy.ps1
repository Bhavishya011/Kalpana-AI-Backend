# Muse Agent Deployment Script for Windows
# Deploys the Muse Agent API to Google Cloud Run

$ErrorActionPreference = "Stop"

Write-Host "🚀 Deploying Muse Agent to Cloud Run..." -ForegroundColor Green

# Configuration
$PROJECT_ID = "nodal-fountain-470717-j1"
$SERVICE_NAME = "muse-agent-api"
$REGION = "us-central1"
$BUCKET_NAME = "kalpana-ai-craft-images"

# Set project
Write-Host "📋 Setting project..." -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

# Check if bucket exists, create if not
Write-Host "📦 Checking GCS bucket..." -ForegroundColor Yellow
$bucketExists = gsutil ls -b gs://$BUCKET_NAME 2>$null
if (-not $bucketExists) {
    Write-Host "Creating bucket $BUCKET_NAME..." -ForegroundColor Yellow
    gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME
    Write-Host "✅ Bucket created" -ForegroundColor Green
} else {
    Write-Host "✅ Bucket already exists" -ForegroundColor Green
}

# Make bucket public (for generated images)
Write-Host "🔓 Setting bucket to public access..." -ForegroundColor Yellow
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME

# Set CORS for browser access
Write-Host "🌐 Setting CORS configuration..." -ForegroundColor Yellow
gsutil cors set cors.json gs://$BUCKET_NAME

# Build and deploy using Cloud Build
Write-Host "🏗️  Building Docker image..." -ForegroundColor Yellow
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
Write-Host "🚢 Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME `
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 4Gi `
    --cpu 2 `
    --timeout 600 `
    --min-instances 0 `
    --max-instances 10 `
    --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Get service URL
$SERVICE_URL = gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)'

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Service URL: $SERVICE_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test endpoints:" -ForegroundColor Yellow
Write-Host "  Health: $SERVICE_URL/health"
Write-Host "  Docs: $SERVICE_URL/docs"
Write-Host "  Generate: POST $SERVICE_URL/generate"
Write-Host ""
