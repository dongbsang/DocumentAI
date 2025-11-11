# Backend - DocumentAI

Flask 기반 백엔드 API 서버

## 📋 디렉토리 구조

```
backend/
├── app/
│   ├── __init__.py           # Flask 앱 생성
│   ├── main.py               # 진입점
│   ├── routers/              # API 엔드포인트
│   │   ├── status.py
│   │   └── upload.py
│   ├── services/             # 비즈니스 로직
│   │   ├── llm_service.py
│   │   ├── ocr_service.py
│   │   ├── pdf_service.py
│   │   ├── word_service.py
│   │   └── ...
│   └── prompt/               # LLM 프롬프트 템플릿
│       ├── resume_info.yaml
│       └── receipt_info.yaml
├── .env                      # 환경 변수 (Git 제외)
└── requirements.txt          # Python 의존성
```

---

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# .env 파일 생성
cd backend
copy ..\.env.example .env  # Windows
# cp ../.env.example .env  # macOS/Linux
```

### 2. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv .venv

# 활성화
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate     # macOS/Linux
```

### 3. 의존성 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 서버 실행

```bash
flask run
```

서버가 `http://localhost:5000`에서 실행됩니다.

---

## 🔌 API 엔드포인트

### GET /api/status
서버 상태 확인

**응답 예시:**
```json
{
  "status": "ok",
  "message": "Backend is running"
}
```

### POST /api/upload
파일 업로드 및 분석

**요청:**
- `file`: 파일 데이터 (multipart/form-data)
- `category`: 문서 카테고리 (이력서, 영수증 등)
- `use_handwriting`: 손글씨 인식 여부 (true/false)

**응답 예시:**
```json
{
  "filename": "resume.pdf",
  "summary": "LLM 분석 결과...",
  "info": "searchable_pdf"
}
```

---

## 🛠️ 개발 모드

디버그 모드로 실행 (자동 리로드):

```bash
# 환경 변수 설정
set FLASK_ENV=development  # Windows
# export FLASK_ENV=development  # macOS/Linux

flask run
```

---

## 📦 주요 의존성

- **Flask 3.1.1**: 웹 프레임워크
- **langchain-ollama**: 로컬 LLM 연동
- **PyMuPDF**: PDF 처리
- **pytesseract / easyocr**: OCR 엔진
- **pillow**: 이미지 처리
- **python-dotenv**: 환경 변수 관리

---

## 🧪 테스트

```bash
# 서버 실행 확인
curl http://localhost:5000/api/status

# 파일 업로드 테스트
curl -X POST http://localhost:5000/api/upload \
  -F "file=@test.pdf" \
  -F "category=resume" \
  -F "use_handwriting=false"
```

---

## ❓ 문제 해결

### 1. Flask 앱을 찾을 수 없음
```bash
# .env 파일 확인
cat .env

# FLASK_APP 변수가 제대로 설정되어 있는지 확인
# FLASK_APP=app.main
```

### 2. 가상환경 활성화 실패
```bash
# PowerShell 실행 정책 오류 시
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Ollama 연결 실패
```bash
# Ollama 서비스 실행 확인
ollama list

# Mistral 모델 다운로드
ollama run mistral
```
