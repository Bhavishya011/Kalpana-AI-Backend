# KalpanaAI Support Chatbot - Cloud Run Deployment Script (PowerShell)

# Configuration
$PROJECT_ID = "nodal-fountain-470717-j1"
$SERVICE_NAME = "support-chatbot-api"
$REGION = "us-central1"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME"

Write-Host "🚀 Deploying KalpanaAI Support Chatbot to Cloud Run..." -ForegroundColor Cyan

# Build the Docker image
Write-Host "📦 Building Docker image..." -ForegroundColor Yellow
gcloud builds submit --tag $IMAGE_NAME --project $PROJECT_ID

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully!" -ForegroundColor Green

# Deploy to Cloud Run
Write-Host "🌐 Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME `
    --image $IMAGE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 2 `
    --timeout 300 `
    --max-instances 10 `
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION" `
    --project $PROJECT_ID

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Deployment successful!" -ForegroundColor Green

# Get the service URL
$SERVICE_URL = gcloud run services describe $SERVICE_NAME `
    --platform managed `
    --region $REGION `
    --format 'value(status.url)' `
    --project $PROJECT_ID

Write-Host ""
Write-Host "🎉 Support Chatbot API is live!" -ForegroundColor Green
Write-Host "📍 URL: $SERVICE_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test endpoints:" -ForegroundColor Yellow
Write-Host "  Health: $SERVICE_URL/health"
Write-Host "  Chat: $SERVICE_URL/chat"
Write-Host "  Quick Help: $SERVICE_URL/quick-help"
Write-Host ""
Write-Host "Test with curl or Postman to verify deployment!" -ForegroundColor Green
