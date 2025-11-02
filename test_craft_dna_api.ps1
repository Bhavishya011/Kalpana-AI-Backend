# Test Craft DNA API Endpoint
$uri = "https://support-chatbot-api-508329185712.us-central1.run.app/api/craft-dna/generate"

$body = @{
    product_id = "TEST_BRASS_DIYA_001"
    artisan_story = "My grandfather taught me the art of brass casting 40 years ago in our family workshop in Moradabad. I continue this 200-year-old family tradition."
    craft_technique = "Traditional lost-wax brass casting with hand-engraving"
    regional_tradition = "Moradabad Brassware - Uttar Pradesh, India"
    materials = "Recycled brass, natural beeswax, clay molds"
    cultural_context = "Diwali ceremonial lamp, symbolizes victory of light over darkness"
    artisan_name = "Rajesh Kumar"
    artisan_village = "Moradabad"
    artisan_state = "Uttar Pradesh"
    artisan_lineage = "4th generation brass artisan"
    years_of_experience = 40
}

Write-Host "`n🧪 Testing Craft DNA API..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"
    
    Write-Host "`n✅ SUCCESS! Craft DNA Generated" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    
    Write-Host "`n📦 Heritage ID:" -ForegroundColor Yellow
    Write-Host "   $($response.heritage_id)" -ForegroundColor White
    
    Write-Host "`n🔗 Heritage URL:" -ForegroundColor Yellow
    Write-Host "   $($response.heritage_url)" -ForegroundColor White
    
    Write-Host "`n📊 Sustainability Score:" -ForegroundColor Yellow
    Write-Host "   $($response.sustainability_score)/100" -ForegroundColor White
    
    if ($response.eco_claims) {
        Write-Host "`n🌱 Eco Claims:" -ForegroundColor Yellow
        $response.eco_claims | ForEach-Object { Write-Host "   • $_" -ForegroundColor White }
    }
    
    Write-Host "`n📜 Heritage Narrative:" -ForegroundColor Yellow
    Write-Host "   Length: $($response.heritage_narrative.Length) characters" -ForegroundColor White
    Write-Host "   Preview: $($response.heritage_narrative.Substring(0, [Math]::Min(200, $response.heritage_narrative.Length)))..." -ForegroundColor Gray
    
    Write-Host "`n🎨 Cultural Significance:" -ForegroundColor Yellow
    if ($response.cultural_significance) {
        $response.cultural_significance.PSObject.Properties | ForEach-Object {
            Write-Host "   • $($_.Name): $($_.Value)" -ForegroundColor White
        }
    }
    
    if ($response.qr_code_base64) {
        Write-Host "`n✅ QR Code Generated:" -ForegroundColor Yellow
        Write-Host "   Base64 length: $($response.qr_code_base64.Length) bytes" -ForegroundColor White
        
        # Save QR code to file
        $qrBytes = [Convert]::FromBase64String($response.qr_code_base64)
        [IO.File]::WriteAllBytes("craft_dna_qr_test.png", $qrBytes)
        Write-Host "   Saved to: craft_dna_qr_test.png" -ForegroundColor Green
    }
    
    # Save full response
    $response | ConvertTo-Json -Depth 10 | Out-File "craft_dna_response.json"
    Write-Host "`n💾 Full response saved to: craft_dna_response.json" -ForegroundColor Green
    
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
    
} catch {
    Write-Host "`n❌ ERROR!" -ForegroundColor Red
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "`n$_" -ForegroundColor Gray
}
