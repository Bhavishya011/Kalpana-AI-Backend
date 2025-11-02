# Simple Test - Craft DNA API with JSON materials
$uri = "https://support-chatbot-api-508329185712.us-central1.run.app/api/craft-dna/generate"

# Convert materials to JSON array format
$materialsJson = '["Recycled brass", "Natural beeswax", "Clay molds"]'

$body = @{
    product_id = "TEST_DIYA_002"
    artisan_story = "My grandfather taught me brass casting 40 years ago in Moradabad"
    craft_technique = "Lost-wax brass casting"
    regional_tradition = "Moradabad Brassware - UP India"
    materials = $materialsJson
    cultural_context = "Diwali ceremonial lamp"
}

Write-Host "Testing Craft DNA API..." -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Body $body
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host "Heritage ID: $($response.craft_dna.heritage_id)" -ForegroundColor Yellow
    Write-Host "Sustainability Score: $($response.craft_dna.sustainability_score)" -ForegroundColor Yellow
    $response | ConvertTo-Json -Depth 10 | Out-File "craft_dna_success.json"
    Write-Host "Saved to craft_dna_success.json" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
}
