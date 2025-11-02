# Artisan Mentor API Deployment Script
# Deploys the Artisan Mentor API to Google Cloud Run

$ErrorActionPreference = "Stop"

Write-Host "Artisan Mentor API Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$PROJECT_ID = "nodal-fountain-470717-j1"
$REGION = "us-central1"
$SERVICE_NAME = "artisan-mentor-api"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME"

Write-Host "Deployment Configuration:" -ForegroundColor Yellow
Write-Host "  Project ID: $PROJECT_ID"
Write-Host "  Region: $REGION"
Write-Host "  Service Name: $SERVICE_NAME"
Write-Host "  Image: $IMAGE_NAME"
Write-Host ""

# Set the active project
Write-Host "Setting Google Cloud project..." -ForegroundColor Green
gcloud config set project $PROJECT_ID

# Build the container image
Write-Host ""
Write-Host "Building container image..." -ForegroundColor Green
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Write-Host ""
gcloud builds submit --tag $IMAGE_NAME

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Container image built successfully!" -ForegroundColor Green

# Deploy to Cloud Run
Write-Host ""
Write-Host "Deploying to Cloud Run..." -ForegroundColor Green
gcloud run deploy $SERVICE_NAME `
    --image $IMAGE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 4Gi `
    --cpu 2 `
    --timeout 600 `
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,CLOUD_STORAGE_BUCKET=kalpana-artisan-tutor"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Deployment failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Deployment successful!" -ForegroundColor Green

# Get the service URL
Write-Host ""
Write-Host "Getting service URL..." -ForegroundColor Green
$SERVICE_URL = gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format "value(status.url)"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Service URL: $SERVICE_URL" -ForegroundColor Yellow
Write-Host ""
Write-Host "Test the API:" -ForegroundColor Yellow
Write-Host "  Health Check: $SERVICE_URL/health" -ForegroundColor Gray
Write-Host "  API Docs: $SERVICE_URL/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "Available Endpoints:" -ForegroundColor Yellow
Write-Host "  POST /start-journey - Start learning journey" -ForegroundColor Gray
Write-Host "  POST /get-lesson - Get interactive lesson" -ForegroundColor Gray
Write-Host "  POST /submit-work - Submit lesson work" -ForegroundColor Gray
Write-Host "  POST /dashboard - Get user dashboard" -ForegroundColor Gray
Write-Host "  POST /analyze-craft - Analyze craft image" -ForegroundColor Gray
Write-Host "  POST /tts - Text to speech" -ForegroundColor Gray
Write-Host "  POST /stt - Speech to text" -ForegroundColor Gray
Write-Host ""
Write-Host "Ready to help artisans!" -ForegroundColor Green
Write-Host ""
