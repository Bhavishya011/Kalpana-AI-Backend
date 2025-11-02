# Deploy Updated Storyteller Agent with Dynamic RAG System
Write-Host "`n🚀 Deploying Updated Storyteller Agent to Cloud Run..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

Write-Host "📦 Changes being deployed:" -ForegroundColor Yellow
Write-Host "  ✅ Dynamic RAG system (no hardcoded keywords)" -ForegroundColor Green
Write-Host "  ✅ Firestore cultural_knowledge_base integration" -ForegroundColor Green
Write-Host "  ✅ Keyword-based document matching" -ForegroundColor Green
Write-Host "  ✅ Improved JSON parsing with fallback" -ForegroundColor Green
Write-Host "  ✅ MAX_TOKENS handling with retry logic" -ForegroundColor Green
Write-Host "  ✅ Shortened prompts (reduced token usage)" -ForegroundColor Green
Write-Host "`n"

$PROJECT_ID = "nodal-fountain-470717-j1"
$REGION = "us-central1"
$SERVICE_NAME = "kalpana-ai-api"

Write-Host "🔧 Configuration:" -ForegroundColor White
Write-Host "  Project: $PROJECT_ID" -ForegroundColor Gray
Write-Host "  Region: $REGION" -ForegroundColor Gray
Write-Host "  Service: $SERVICE_NAME" -ForegroundColor Gray
Write-Host "`n"

$confirm = Read-Host "Continue with deployment? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "❌ Deployment cancelled.`n" -ForegroundColor Red
    exit 0
}

Write-Host "`n🔨 Building Docker image..." -ForegroundColor Yellow

try {
    # Build and deploy using gcloud
    gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME --project=$PROJECT_ID
    
    if ($LASTEXITCODE -ne 0) {
        throw "Docker build failed"
    }
    
    Write-Host "`n✅ Docker image built successfully!" -ForegroundColor Green
    Write-Host "`n🚀 Deploying to Cloud Run..." -ForegroundColor Yellow
    
    gcloud run deploy $SERVICE_NAME `
        --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
        --platform managed `
        --region $REGION `
        --allow-unauthenticated `
        --memory 2Gi `
        --cpu 2 `
        --timeout 300 `
        --max-instances 10 `
        --min-instances 1 `
        --port 8080 `
        --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID,PORT=8080 `
        --project=$PROJECT_ID
    
    if ($LASTEXITCODE -ne 0) {
        throw "Cloud Run deployment failed"
    }
    
    Write-Host "`n✅ Deployment completed successfully!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray
    
    # Get service URL
    $SERVICE_URL = gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format "value(status.url)" --project=$PROJECT_ID
    
    Write-Host "🌐 Service URL: $SERVICE_URL" -ForegroundColor Cyan
    Write-Host "`n🧪 Testing deployment..." -ForegroundColor Yellow
    
    Start-Sleep -Seconds 5  # Wait for service to be ready
    
    # Test health endpoint
    try {
        $health = Invoke-RestMethod -Uri "$SERVICE_URL/health" -Method Get -TimeoutSec 30
        Write-Host "✅ API is healthy!" -ForegroundColor Green
        Write-Host "`nAgent Status:" -ForegroundColor White
        
        if ($health.agent_status) {
            foreach ($agent in $health.agent_status.PSObject.Properties) {
                $status = if ($agent.Value -eq "available") { "✅" } else { "❌" }
                Write-Host "  $status $($agent.Name): $($agent.Value)" -ForegroundColor Gray
            }
        }
    } catch {
        Write-Host "⚠️  Health check failed (service may still be starting): $_" -ForegroundColor Yellow
    }
    
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "🎉 Storyteller Agent Updated Successfully!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray
    
    Write-Host "📚 What's New:" -ForegroundColor Yellow
    Write-Host "  • Stories are now unique for each art form" -ForegroundColor Green
    Write-Host "  • Uses Firestore cultural_knowledge_base dynamically" -ForegroundColor Green
    Write-Host "  • No more hardcoded keywords or regions" -ForegroundColor Green
    Write-Host "  • Easily expandable - just add docs to Firestore" -ForegroundColor Green
    Write-Host "`n"
    
    Write-Host "🧪 Test the API:" -ForegroundColor Yellow
    Write-Host "  curl -X POST $SERVICE_URL/api/storytelling -F 'image=@your_image.jpg' -F 'description=blue pottery from Jaipur'" -ForegroundColor Gray
    Write-Host "`n"
    
    Write-Host "📋 View logs:" -ForegroundColor Yellow
    Write-Host "  gcloud run logs read $SERVICE_NAME --region $REGION --limit 50 --project=$PROJECT_ID" -ForegroundColor Gray
    Write-Host "`n"
    
} catch {
    Write-Host "`n❌ Deployment failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Gray
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check authentication: gcloud auth list" -ForegroundColor Gray
    Write-Host "  2. Check project: gcloud config get-value project" -ForegroundColor Gray
    Write-Host "  3. Check Cloud Build API is enabled" -ForegroundColor Gray
    Write-Host "  4. Check Cloud Run API is enabled" -ForegroundColor Gray
    Write-Host "  5. Review logs: gcloud builds log --limit 50`n" -ForegroundColor Gray
    exit 1
}
