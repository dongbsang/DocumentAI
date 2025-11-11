# Ollama CPU 모드 시작 스크립트

Write-Host "🚀 Ollama 서버 시작 중 (CPU 모드)..." -ForegroundColor Green

# CPU 모드 설정
$env:OLLAMA_NUM_GPU=0
Write-Host "✅ OLLAMA_NUM_GPU=0 설정 완료" -ForegroundColor Cyan

# Ollama 서비스 시작
Write-Host "🤖 Ollama 서버 실행 중..." -ForegroundColor Yellow
Write-Host "   종료하려면 Ctrl+C를 누르세요" -ForegroundColor White
Write-Host ""

ollama serve
