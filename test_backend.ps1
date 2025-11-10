# Test if backend is responding

Write-Host "Testing backend..." -ForegroundColor Cyan

# Test root endpoint
Write-Host "`n1. Testing root endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -Method GET -UseBasicParsing
    Write-Host "✓ Root endpoint OK: $($response.StatusCode)" -ForegroundColor Green
    $response.Content
} catch {
    Write-Host "✗ Root endpoint failed: $_" -ForegroundColor Red
}

# Test health endpoint
Write-Host "`n2. Testing health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -UseBasicParsing
    Write-Host "✓ Health endpoint OK: $($response.StatusCode)" -ForegroundColor Green
    $response.Content
} catch {
    Write-Host "✗ Health endpoint failed: $_" -ForegroundColor Red
}

# Test languages endpoint
Write-Host "`n3. Testing languages endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/languages" -Method GET -UseBasicParsing
    Write-Host "✓ Languages endpoint OK: $($response.StatusCode)" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
} catch {
    Write-Host "✗ Languages endpoint failed: $_" -ForegroundColor Red
}

Write-Host "`n" -NoNewline
Read-Host "Press Enter to exit"
