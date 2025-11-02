# Quick Deploy Script for Artisan Mentor Backend
# This script deploys the fixed backend to Google Cloud Run

Write-Host "`n🚀 Starting Deployment to Google Cloud Run..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

# Check if we're in the right directory
$currentPath = Get-Location
if ($currentPath.Path -notlike "*Exchange*") {
    Write-Host "⚠️  Not in Exchange directory. Navigating..." -ForegroundColor Yellow
    cd ..\Exchange
}

Write-Host "📍 Current directory: $(Get-Location)`n" -ForegroundColor Gray

# Confirm deployment
Write-Host "This will deploy the Artisan Mentor API with:" -ForegroundColor White
Write-Host "  • Dashboard NoneType fixes" -ForegroundColor Gray
Write-Host "  • Progress persistence fixes" -ForegroundColor Gray
Write-Host "  • Starting lesson fixes`n" -ForegroundColor Gray

$confirm = Read-Host "Continue with deployment? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "❌ Deployment cancelled.`n" -ForegroundColor Red
    exit 0
}

Write-Host "`n🔨 Building and deploying..." -ForegroundColor Yellow

# Deploy to Cloud Run
try {
    gcloud run deploy artisan-mentor-api `
        --source . `
        --region us-central1 `
        --platform managed `
        --allow-unauthenticated `
        --set-env-vars "GOOGLE_CLOUD_PROJECT=nodal-fountain-470717-j1,CLOUD_STORAGE_BUCKET=kalpana-artisan-tutor"
    
    Write-Host "`n✅ Deployment completed successfully!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray
    
    # Test the deployment
    Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow
    $health = Invoke-RestMethod -Uri "https://artisan-mentor-api-508329185712.us-central1.run.app/health" -Method Get
    
    if ($health.status -eq "healthy") {
        Write-Host "✅ API is healthy and running!" -ForegroundColor Green
        Write-Host "`nAPI URL: https://artisan-mentor-api-508329185712.us-central1.run.app" -ForegroundColor Cyan
        Write-Host "`n🎉 Your backend is now fixed and deployed!" -ForegroundColor Green
        Write-Host "`nNext steps:" -ForegroundColor Yellow
        Write-Host "  1. Run .\test_backend_fixes.ps1 to verify all fixes" -ForegroundColor Gray
        Write-Host "  2. Test your frontend - it should now sync with backend" -ForegroundColor Gray
        Write-Host "  3. Dashboard should load without errors`n" -ForegroundColor Gray
    } else {
        Write-Host "⚠️  API deployed but health check failed" -ForegroundColor Yellow
        Write-Host "Status: $($health.status)`n" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "`n❌ Deployment failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Gray
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check if you're logged in: gcloud auth list" -ForegroundColor Gray
    Write-Host "  2. Check project: gcloud config get-value project" -ForegroundColor Gray
    Write-Host "  3. Make sure you're in the Exchange directory`n" -ForegroundColor Gray
    exit 1
}
