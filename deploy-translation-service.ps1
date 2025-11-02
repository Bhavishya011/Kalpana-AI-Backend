# Deploy Translation Service (Separate from Main API)
# PowerShell Script

Write-Host "🌐 Deploying KalpanaAI Translation Service..." -ForegroundColor Cyan
Write-Host "This service is separate from the main product pipeline" -ForegroundColor Yellow
Write-Host ""

# Step 1: Build Docker image
Write-Host "🔨 Building Translation Service Docker image..." -ForegroundColor Cyan
gcloud builds submit `
    --tag gcr.io/nodal-fountain-470717-j1/kalpana-translation `
    --dockerfile Dockerfile.translation `
    .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Deploy to Cloud Run (separate service)
Write-Host "🚀 Deploying Translation Service to Cloud Run..." -ForegroundColor Cyan
gcloud run deploy kalpana-translation `
    --image gcr.io/nodal-fountain-470717-j1/kalpana-translation `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --memory 1Gi `
    --cpu 1 `
    --timeout 60 `
    --max-instances 5 `
    --min-instances 0 `
    --port 8081 `
    --set-env-vars GOOGLE_CLOUD_PROJECT=nodal-fountain-470717-j1,PORT=8081

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Cloud Run deployment failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Translation Service deployed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Service Details:" -ForegroundColor Cyan
Write-Host "  - Service Name: kalpana-translation"
Write-Host "  - Separate from: kalpana-ai-api (main product pipeline)"
Write-Host "  - Port: 8081"
Write-Host "  - Memory: 1Gi (lighter than main API)"
Write-Host "  - Endpoint: https://kalpana-translation-508329185712.us-central1.run.app"
Write-Host ""
Write-Host "🧪 Test the service:" -ForegroundColor Yellow
Write-Host '  curl -X POST https://kalpana-translation-508329185712.us-central1.run.app/translate \'
Write-Host '    -H "Content-Type: application/json" \'
Write-Host '    -d "{\"text\": \"Hello\", \"targetLocale\": \"hi-IN\"}"'
Write-Host ""
Write-Host "✨ Translation service is now live and independent!" -ForegroundColor Green
