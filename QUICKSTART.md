# 🚀 빠른 시작 가이드

DocumentAI를 5분 안에 실행하는 방법

---

## ✅ 사전 요구사항

- Python 3.10 이상
- Node.js 16 이상
- Ollama 설치됨
- (Windows) Microsoft Word 설치 (Word 문서 변환용)

---

## 📦 1단계: 설치

### Windows PowerShell
```powershell
# 1. backend 설정
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# 2. frontend 설정
cd frontend
npm install
cd ..
```

### macOS/Linux
```bash
# 1. backend 설정
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# 2. frontend 설정
cd frontend
npm install
cd ..
```

---

## 🤖 2단계: Ollama 모델 다운로드

```bash
ollama run mistral
```

모델 다운로드 확인:
```bash
ollama list
```

---

## 🎯 3단계: 실행

### 터미널 1: Backend 실행

```powershell
# Windows
cd backend
.\.venv\Scripts\Activate.ps1
flask run
```

```bash
# macOS/Linux
cd backend
source .venv/bin/activate
flask run
```

✅ Backend: `http://localhost:5000` 실행 확인

---

### 터미널 2: Frontend 실행 (새 터미널)

```bash
cd frontend
npm start
```

✅ Frontend: `http://localhost:3000` 자동으로 브라우저 열림

---

## 🎉 완료!

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api

---

## 🛑 종료

각 터미널에서 `Ctrl + C`

---

## ❓ 문제 발생 시

### 1. Ollama 연결 실패
```bash
# Ollama 실행 확인
ollama list

# 모델 재다운로드
ollama pull mistral
```

### 2. 포트 충돌
```bash
# Windows
netstat -ano | findstr :5000
netstat -ano | findstr :3000

# macOS/Linux
lsof -i :5000
lsof -i :3000
```

### 3. Python 가상환경 활성화 오류 (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. GPU 관련 오류 (EasyOCR)
EasyOCR은 기본적으로 CPU 모드로 설정되어 있습니다. GPU를 사용하려면 `ocr_service.py`에서 `gpu=True`로 변경하세요.

### 5. Word 문서 변환 실패
Windows에서 Microsoft Word가 설치되어 있어야 합니다. Word가 없으면 `.docx` 파일 변환이 실패할 수 있습니다.

---

## 📝 지원 파일 형식

- ✅ PDF (검색 가능한 PDF, 스캔된 PDF)
- ✅ 이미지 (JPG, PNG, BMP, TIFF 등)
- ✅ Word 문서 (.docx) - Windows + MS Word 필요
- ⚠️ HWP (향후 지원 예정)
