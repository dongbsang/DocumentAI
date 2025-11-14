#!/bin/bash

echo "========================================"
echo "🚀 DocumentAI 빌드 스크립트 (Linux/macOS)"
echo "========================================"
echo ""

# 에러 발생 시 스크립트 중단
set -e

# ========================================
# Step 1: 프론트엔드 빌드
# ========================================
echo "[Step 1/5] 📦 프론트엔드 빌드 중..."
cd frontend
npm install
npm run build
echo "✅ 프론트엔드 빌드 완료"
cd ..
echo ""

# ========================================
# Step 2: 백엔드 빌드 (PyInstaller)
# ========================================
echo "[Step 2/5] 📦 백엔드 빌드 중..."
cd backend

# 가상환경 활성화
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "⚠️  가상환경을 찾을 수 없습니다. 글로벌 Python 사용"
fi

# PyInstaller 설치 확인
if ! pip show pyinstaller > /dev/null 2>&1; then
    echo "PyInstaller 설치 중..."
    pip install pyinstaller
fi

# 이전 빌드 결과 삭제
rm -rf dist build

# PyInstaller로 빌드
pyinstaller ../build-scripts/build-backend.spec
echo "✅ 백엔드 빌드 완료"
cd ..
echo ""

# ========================================
# Step 3: Ollama 준비
# ========================================
echo "[Step 3/5] 📦 Ollama 준비 중..."

if [ ! -d "ollama" ]; then
    echo "⚠️  Ollama를 수동으로 준비해야 합니다."
    echo ""
    echo "다음 단계를 따라주세요:"
    echo "1. https://ollama.com/download 에서 해당 OS 버전 다운로드"
    echo "2. ollama 실행 파일을 ollama/ 디렉토리에 복사"
    echo "3. 'ollama pull mistral' 실행하여 모델 다운로드"
    echo ""
    read -p "Ollama가 준비되면 Enter를 눌러 계속..."
else
    echo "✅ Ollama 디렉토리 존재 확인"
fi

if [ ! -d "ollama/models" ]; then
    echo "⚠️  models 디렉토리가 없습니다."
    echo "Mistral 모델을 다운로드하려면 'ollama pull mistral'를 실행하세요."
    read -p "Enter를 눌러 계속..."
else
    echo "✅ Models 디렉토리 확인"
fi
echo ""

# ========================================
# Step 4: Electron 의존성 설치
# ========================================
echo "[Step 4/5] 📦 Electron 의존성 설치 중..."
cd electron
npm install
echo "✅ Electron 의존성 설치 완료"
cd ..
echo ""

# ========================================
# Step 5: Electron 앱 빌드
# ========================================
echo "[Step 5/5] 📦 Electron 앱 빌드 중..."
cd electron

# OS별 빌드
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    npm run build:linux
    echo "✅ Linux용 빌드 완료"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    npm run build:mac
    echo "✅ macOS용 빌드 완료"
else
    echo "⚠️  알 수 없는 OS: $OSTYPE"
fi

cd ..
echo ""

# ========================================
# 빌드 완료
# ========================================
echo "========================================"
echo "✅ 빌드 완료!"
echo "========================================"
echo ""
echo "📂 실행 파일 위치: electron/dist/"
echo ""
