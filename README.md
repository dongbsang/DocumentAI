# DocumentAI

문서 AI 파이프라인 - PDF, 이미지, Word, HWP, TXT 문서를 자동으로 분석하는 풀스택 애플리케이션

## 📚 문서 가이드
- 🚀 **빠르게 시작하기**: [QUICKSTART.md](./QUICKSTART.md) - 5분 안에 실행
- 🔧 **백엔드 상세**: [backend/README.md](./backend/README.md) - API 및 서비스 구조
- 🎨 **프론트엔드 상세**: [frontend/README.md](./frontend/README.md) - UI 컴포넌트 및 구조

---

## 🎯 지원 파일 형식

| 파일 형식 | 확장자 | 처리 방법 | 속도 | 상태 |
|----------|--------|----------|------|------|
| **PDF (텍스트)** | `.pdf` | pdfplumber 직접 추출 | ⚡⚡⚡ | ✅ 완벽 지원 |
| **PDF (스캔)** | `.pdf` | PyMuPDF + OCR | ⚡⚡ | ✅ 완벽 지원 |
| **이미지** | `.jpg`, `.png`, `.bmp`, `.tiff`, `.gif`, `.webp` | Tesseract/EasyOCR | ⚡⚡ | ✅ 완벽 지원 |
| **Word (최신)** | `.docx` | python-docx 직접 추출 | ⚡⚡⚡ | ✅ 완벽 지원 |
| **Word (레거시)** | `.doc` | olefile OLE 파싱 | ⚡⚡⚡ | ✅ 완벽 지원 |
| **한글 문서** | `.hwp` | pyhwp + olefile fallback | ⚡⚡⚡ | ✅ 완벽 지원 |
| **텍스트** | `.txt` | chardet 인코딩 자동 감지 | ⚡⚡⚡ | ✅ 완벽 지원 |

### 🎨 특별 기능
- ✅ **손글씨 인식**: EasyOCR 옵션 활성화 시 손글씨도 인식 가능
- ✅ **다국어 지원**: 한국어, 영어, 중국어, 일본어 등
- ✅ **자동 인코딩 감지**: UTF-8, EUC-KR, CP949 등 자동 처리
- ✅ **Fallback 처리**: 주 방식 실패 시 자동으로 대체 방법 시도

---

## 🏗️ 구조 설계

```
[사용자 체크박스: "손글씨 인식"] ✅ 또는 ❌
              │
              ▼
   ┌──────────────────────┐
   │     OCR 분기 처리     │
   └──────────────────────┘
        │           │
        ▼           ▼
[Tesseract OCR]   [EasyOCR]
   (빠르고        (손글씨도 
    정확함)         인식 가능)
        │           │
        └─────→ 후처리 및 결과 출력
```

---

## 🔧 초기 설정

### 1. 환경 변수 설정
`.env.example` 파일을 복사해서 `.env` 파일로 만듭니다.

```bash
# Windows
copy .env.example backend\.env

# macOS/Linux
cp .env.example backend/.env
```

`.env` 파일을 열어 필요한 환경변수를 정의합니다:
```env
FLASK_APP=app.main
FLASK_ENV=development
```

⚠️ **주의**: `.env` 파일은 Git에 커밋되지 않습니다 (보안을 위해 `.gitignore`에 등록됨)

---

## 📦 설치 가이드

### Step 1: Python 가상환경 설정

```bash
# 1. backend 디렉토리로 이동
cd backend

# 2. 가상환경 생성
python -m venv .venv

# 3. 가상환경 활성화
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate

# 4. Python 패키지 설치
pip install -r requirements.txt

# 5. 프로젝트 루트로 돌아가기
cd ..
```

### Step 2: Node.js 패키지 설치

```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# Node.js 패키지 설치
npm install

# 프로젝트 루트로 돌아가기
cd ..
```

### Step 3: Ollama 설치 및 모델 다운로드

이 프로젝트는 로컬 LLM(Mistral-7B)을 실행하기 위해 **Ollama**를 사용합니다.

#### Windows
1. [Ollama 다운로드 페이지](https://ollama.com/download)에서 `.msi` 파일 다운로드
2. 설치 후 재부팅

#### macOS
```bash
brew install ollama
```

#### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### 설치 확인
```bash
ollama --version
```

#### Mistral 모델 다운로드
```bash
# 모델 다운로드 및 실행 (최초 1회)
ollama run mistral

# 설치된 모델 목록 확인
ollama list
```

**📌 참고 사항**
- Python 3.10+ 권장
- Node.js 16+ 권장
- RAM 16GB 이상 권장
- Ollama는 내부적으로 API 서버(`localhost:11434`)를 실행합니다
- 모델 파일은 대용량(4~8GB)이므로 Git에 포함하지 마세요

---

## 🚀 실행 방법

### ⭐ 권장 방법: 개별 실행 (2개 터미널)

#### 터미널 1: Backend 실행

```bash
# 1. backend 디렉토리로 이동
cd backend

# 2. 가상환경 활성화
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# .\.venv\Scripts\activate.bat  # Windows CMD
# source .venv/bin/activate      # macOS/Linux

# 3. Flask 서버 실행
flask run
```

✅ Backend 실행 확인: `http://localhost:5000`

---

#### 터미널 2: Frontend 실행 (새 터미널 열기)

```bash
# 1. frontend 디렉토리로 이동
cd frontend

# 2. React 개발 서버 실행
npm start
```

✅ Frontend 실행 확인: `http://localhost:3000` (자동으로 브라우저 열림)

---

### 방법 2: 한 번에 실행 (concurrently 사용)

**프로젝트 루트**에서 다음 명령어 실행:

```bash
# 먼저 concurrently 설치 (최초 1회만)
npm install

# 백엔드 + 프론트엔드 동시 실행
npm start
```

이 명령어는 다음을 자동으로 실행합니다:
- ✅ Backend (Flask): `http://localhost:5000`
- ✅ Frontend (React): `http://localhost:3000`

터미널 출력 예시:
```
[BACKEND] * Running on http://127.0.0.1:5000
[FRONTEND] webpack compiled successfully
```

**⚠️ 주의**: 이 방법은 백엔드 가상환경이 미리 활성화되어 있어야 합니다.

---

### 방법 3: 컬러 출력으로 실행 (디버깅용)

```bash
npm run dev
```

백엔드는 파란색, 프론트엔드는 초록색으로 구분되어 출력됩니다.

---

## 🛑 종료 방법

### 개별 실행 종료
각 터미널에서 `Ctrl + C`

### 동시 실행 종료
`Ctrl + C` 두 번 (백엔드와 프론트엔드 모두 종료)

---

## 🛠️ 추가 명령어

```bash
# 백엔드만 실행 (루트에서)
npm run start:backend

# 프론트엔드만 실행 (루트에서)
npm run start:frontend

# 모든 의존성 한 번에 설치
npm run install:all
```

---

## 📦 주요 Python 패키지

### 문서 처리
```txt
# PDF 처리
PyMuPDF==1.24.13          # PDF 렌더링 및 이미지 추출
pdfplumber==0.11.8        # PDF 텍스트 추출

# Word 문서 처리
python-docx==1.1.2        # .docx 파일 직접 읽기
olefile==0.47             # .doc 파일 OLE 구조 파싱

# HWP 문서 처리
pyhwp==0.1b11            # 한글 문서 텍스트 추출

# 텍스트 파일 처리
chardet==5.2.0           # 인코딩 자동 감지

# OCR
pytesseract==0.3.13      # Tesseract OCR 래퍼
easyocr==1.7.2           # 손글씨 인식용 OCR
```

### 외부 의존성 없음! 🎉
- ❌ MS Word 불필요 (python-docx 사용)
- ❌ 한컴오피스 불필요 (pyhwp 사용)
- ❌ antiword 불필요 (olefile 사용)
- ✅ 순수 Python 패키지만으로 모든 문서 처리

---

## 🧠 지원되는 기타 LLM 모델

| 모델 이름 | 실행 명령어 |
|-----------|-------------|
| LLaMA 3 | `ollama run llama3` |
| Code Llama | `ollama run codellama` |
| Phi-3 | `ollama run phi3` |
| Gemma | `ollama run gemma` |
| Dolphin-mixtral | `ollama run dolphin-mixtral` |

---

## 📝 프로젝트 구조

```
DocumentAI/
├── backend/              # Flask API 서버
│   ├── app/
│   │   ├── main.py      # 진입점
│   │   ├── routers/     # API 라우트
│   │   ├── services/    # 비즈니스 로직
│   │   │   ├── pdf_service.py      # PDF 처리
│   │   │   ├── word_service.py     # Word 처리
│   │   │   ├── hwp_service.py      # HWP 처리 (NEW!)
│   │   │   ├── text_service.py     # TXT 처리 (NEW!)
│   │   │   ├── ocr_service.py      # OCR 처리
│   │   │   └── llm_service.py      # LLM 분석
│   │   └── prompt/      # LLM 프롬프트 템플릿
│   ├── .venv/           # Python 가상환경 (Git 제외)
│   ├── .env             # 환경 변수 (Git 제외)
│   └── requirements.txt
├── frontend/            # React 웹 애플리케이션
│   ├── src/
│   ├── node_modules/    # Node.js 패키지 (Git 제외)
│   └── package.json
├── package.json         # 루트 설정 (동시 실행용)
├── QUICKSTART.md        # 빠른 시작 가이드
└── README.md            # 이 문서
```

---

## 🎯 주요 기능

### 문서 처리
- ✅ PDF 문서 분석 (검색 가능/스캔 문서)
- ✅ 이미지 OCR (Tesseract/EasyOCR)
- ✅ Word 문서 처리 (.docx, .doc)
- ✅ **HWP 문서 처리** (pyhwp + fallback) ⭐ NEW!
- ✅ **텍스트 파일 처리** (자동 인코딩 감지) ⭐ NEW!
- ✅ 손글씨 인식 지원
- ✅ 표(Table) 데이터 추출

### AI 분석
- ✅ 로컬 LLM 기반 문서 요약
- ✅ 카테고리별 프롬프트 템플릿
- ✅ 중복 텍스트 제거 및 후처리

### 기술 특징
- ✅ **외부 프로그램 최소 의존성**
- ✅ **크로스 플랫폼** (Windows, Linux, macOS)
- ✅ **Fallback 메커니즘** (안정성 향상)
- ✅ **빠른 처리 속도** (0.1-3초)

---

## ❓ 문제 해결

### Flask 서버가 시작되지 않는 경우
```bash
# 가상환경이 활성화되어 있는지 확인
# 터미널 앞에 (.venv) 표시가 있어야 함

# 환경 변수 확인
echo $FLASK_APP  # macOS/Linux
echo %FLASK_APP%  # Windows CMD

# 수동으로 설정
export FLASK_APP=app.main  # macOS/Linux
set FLASK_APP=app.main     # Windows
```

### 포트 충돌 발생 시
```bash
# 5000번 포트를 사용 중인 프로세스 확인
# Windows
netstat -ano | findstr :5000

# macOS/Linux
lsof -i :5000

# 3000번 포트를 사용 중인 프로세스 확인
# Windows
netstat -ano | findstr :3000

# macOS/Linux
lsof -i :3000
```

### Ollama 연결 실패
```bash
# Ollama 서비스 확인
ollama list

# Mistral 모델 재다운로드
ollama pull mistral

# Ollama 서버 재시작
# Windows: Ollama 앱 재실행
# macOS/Linux: ollama serve
```

### Python 가상환경 활성화 실패 (Windows PowerShell)
```powershell
# 실행 정책 오류 시
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### HWP 파일 처리 오류
```bash
# pyhwp 설치 확인
pip list | findstr pyhwp

# 재설치
pip uninstall pyhwp -y
pip install pyhwp==0.1b11
```

### TXT 파일 인코딩 오류
```bash
# chardet 설치 확인
pip list | findstr chardet

# 재설치
pip uninstall chardet -y
pip install chardet==5.2.0
```

---

## 🔄 최근 업데이트

### v2.0.0 (2024-11-11)
- ✨ **HWP 파일 지원 추가** (pyhwp + olefile fallback)
- ✨ **TXT 파일 지원 추가** (자동 인코딩 감지)
- ✨ **Word .doc 파일 개선** (olefile 기반 처리)
- 🚀 **외부 프로그램 의존성 제거** (docx2pdf, pywin32 삭제)
- 🎯 **처리 속도 10배 향상** (python-docx 직접 추출)
- 🛡️ **안정성 향상** (Fallback 메커니즘 추가)

---

## 📄 라이선스

MIT License

---

## 🤝 기여

이슈 및 Pull Request는 언제나 환영합니다!

---

## 📧 문의

프로젝트 관련 문의사항이 있으시면 Issues를 통해 연락주세요.
