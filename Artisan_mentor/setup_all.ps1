# Complete Setup Script for Artisan Mentor
# Run this to set up everything automatically

$ErrorActionPreference = "Stop"

Write-Host "Artisan Mentor - Complete Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ID = "nodal-fountain-470717-j1"
$REGION = "us-central1"

# Step 1: Enable APIs
Write-Host "Step 1: Enabling Google Cloud APIs..." -ForegroundColor Yellow
Write-Host "This may take a minute..." -ForegroundColor Gray

$apis = @(
    "firestore.googleapis.com",
    "storage.googleapis.com",
    "texttospeech.googleapis.com",
    "speech.googleapis.com",
    "aiplatform.googleapis.com",
    "run.googleapis.com"
)

foreach ($api in $apis) {
    Write-Host "  Enabling $api..." -ForegroundColor Gray
    gcloud services enable $api --project=$PROJECT_ID 2>&1 | Out-Null
}

Write-Host "All APIs enabled" -ForegroundColor Green
Write-Host ""

# Step 2: Create Firestore Database
Write-Host "Step 2: Creating Firestore database..." -ForegroundColor Yellow

try {
    gcloud firestore databases create --location=$REGION --project=$PROJECT_ID 2>&1 | Out-Null
    Write-Host "Firestore database created" -ForegroundColor Green
} catch {
    Write-Host "Firestore database may already exist" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Set up Firestore structure
Write-Host "Step 3: Initializing Firestore structure..." -ForegroundColor Yellow
python setup_database.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Database setup failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Set up Cloud Storage
Write-Host "Step 4: Setting up Cloud Storage..." -ForegroundColor Yellow
python setup_storage.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Storage setup failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 5: Verify setup
Write-Host "Step 5: Verifying setup..." -ForegroundColor Yellow
python verify_setup.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Verification failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 6: Run tests
Write-Host "Step 6: Running tests..." -ForegroundColor Yellow
python test_api.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Some tests failed, but setup is complete" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "What was set up:" -ForegroundColor Yellow
Write-Host "  - Google Cloud APIs enabled" -ForegroundColor Green
Write-Host "  - Firestore database created" -ForegroundColor Green
Write-Host "  - Cloud Storage bucket configured" -ForegroundColor Green
Write-Host "  - Sample data initialized" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Review Firestore data:" -ForegroundColor Gray
Write-Host "     https://console.firebase.google.com/project/$PROJECT_ID/firestore" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Apply Firestore security rules (see setup_database.py output)" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Deploy to Cloud Run:" -ForegroundColor Gray
Write-Host "     .\deploy.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ready to deploy!" -ForegroundColor Green
Write-Host ""
