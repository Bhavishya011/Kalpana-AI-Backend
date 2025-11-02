# Test Backend Fixes Script
# Run this AFTER deploying to verify all fixes work

$API_URL = "https://artisan-mentor-api-508329185712.us-central1.run.app"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🧪 TESTING BACKEND FIXES" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$API_URL/health" -Method Get
    Write-Host "✅ Health check passed" -ForegroundColor Green
    Write-Host "   Status: $($health.status)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Health check failed: $_" -ForegroundColor Red
    exit 1
}

# Test 2: Start Journey (Fix #3 - Starting Lesson)
Write-Host "`nTest 2: Start Journey - Starting Lesson Fix" -ForegroundColor Yellow
$userId = "test_fix_$(Get-Random -Minimum 1000 -Maximum 9999)"
$profile = @{
    user_id = $userId
    name = "Test User"
    learning_style = "visual"
    language = "en"
    current_skill_level = "beginner"
} | ConvertTo-Json

try {
    $startResult = Invoke-RestMethod -Uri "$API_URL/start-journey" -Method Post -Body $profile -ContentType "application/json"
    $startingLesson = $startResult.starting_point.lesson
    
    if ($startingLesson -and $startingLesson -ne "") {
        Write-Host "✅ Starting lesson fix works!" -ForegroundColor Green
        Write-Host "   Starting lesson: $startingLesson" -ForegroundColor Gray
    } else {
        Write-Host "❌ Starting lesson is still empty!" -ForegroundColor Red
        Write-Host "   Value: '$startingLesson'" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Start journey failed: $_" -ForegroundColor Red
}

# Wait for Firestore to sync
Write-Host "`n⏳ Waiting 3 seconds for Firestore sync..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# Test 3: Submit Work (Fix #2 - Progress Persistence)
Write-Host "`nTest 3: Submit Work - Progress Persistence Fix" -ForegroundColor Yellow
$submission = @{
    user_id = $userId
    lesson_id = $startingLesson
    submission = @{
        content = "Test submission to verify progress tracking"
        metadata = @{
            type = "text"
            timestamp = (Get-Date).ToString("o")
        }
    }
} | ConvertTo-Json -Depth 5

try {
    $submitResult = Invoke-RestMethod -Uri "$API_URL/submit-work" -Method Post -Body $submission -ContentType "application/json"
    
    if ($submitResult.passed) {
        Write-Host "✅ Submission passed!" -ForegroundColor Green
        Write-Host "   Points earned: $($submitResult.points_earned)" -ForegroundColor Gray
    } else {
        Write-Host "⚠️  Submission did not pass (this is OK for testing)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Submit work failed: $_" -ForegroundColor Red
}

# Wait for progress update
Write-Host "`n⏳ Waiting 2 seconds for progress update..." -ForegroundColor Gray
Start-Sleep -Seconds 2

# Test 4: Dashboard (Fix #1 - NoneType Error)
Write-Host "`nTest 4: Dashboard - NoneType Error Fix" -ForegroundColor Yellow
$dashboardRequest = @{
    user_id = $userId
} | ConvertTo-Json

try {
    $dashResult = Invoke-RestMethod -Uri "$API_URL/dashboard" -Method Post -Body $dashboardRequest -ContentType "application/json"
    
    if ($dashResult.status -eq "success") {
        Write-Host "✅ Dashboard fix works!" -ForegroundColor Green
        Write-Host "   Learning Progress:" -ForegroundColor Gray
        Write-Host "     - Total Points: $($dashResult.dashboard.learning_progress.total_points)" -ForegroundColor Gray
        Write-Host "     - Completed Lessons: $($dashResult.dashboard.learning_progress.completed_lessons)" -ForegroundColor Gray
        Write-Host "     - Completion %: $($dashResult.dashboard.learning_progress.completion_percentage)%" -ForegroundColor Gray
        Write-Host "     - Current Level: $($dashResult.dashboard.learning_progress.current_level)" -ForegroundColor Gray
        Write-Host "   Business Metrics:" -ForegroundColor Gray
        Write-Host "     - Photography: $($dashResult.dashboard.business_metrics.business_readiness.photography)" -ForegroundColor Gray
        Write-Host "   Skill Matrix:" -ForegroundColor Gray
        Write-Host "     - Overall Readiness: $($dashResult.dashboard.skill_development.overall_readiness)" -ForegroundColor Gray
    } else {
        Write-Host "❌ Dashboard returned error: $($dashResult.message)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Dashboard failed: $_" -ForegroundColor Red
    Write-Host "   Error details: $($_.Exception.Message)" -ForegroundColor Gray
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "📊 TEST SUMMARY" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "User ID tested: $userId" -ForegroundColor Gray
Write-Host "Starting lesson: $startingLesson" -ForegroundColor Gray
Write-Host "`nIf all tests passed, backend is fixed! 🎉" -ForegroundColor Green
Write-Host "Your frontend will now sync with backend properly.`n" -ForegroundColor White
