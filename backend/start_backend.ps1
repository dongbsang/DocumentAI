# Flask 백엔드 시작 스크립트

Write-Host "🚀 DocumentAI 백엔드 시작 중..." -ForegroundColor Green

# 1. 가상환경 활성화
Write-Host "📦 가상환경 활성화 중..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# 2. 환경 확인
Write-Host "🔍 Python 버전:" -ForegroundColor Yellow
python --version

# 3. Ollama CPU 모드 설정
Write-Host "⚙️ Ollama CPU 모드 설정..." -ForegroundColor Cyan
$env:OLLAMA_NUM_GPU=0

# 4. Flask 서버 시작
Write-Host "🌐 Flask 서버 시작 (포트 5000)..." -ForegroundColor Green
Write-Host "   접속 주소: http://localhost:5000" -ForegroundColor White
Write-Host "   종료: Ctrl+C" -ForegroundColor White
Write-Host ""

python app/main.py
