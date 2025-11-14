# DocumentAI

문서 AI 파이프라인 - PDF, 이미지, Word, HWP, TXT 문서를 자동으로 분석하는 풀스택 애플리케이션

## 📚 문서 가이드
- 🚀 **빠르게 시작하기**: [QUICKSTART.md](./QUICKSTART.md) - 5분 안에 실행
- 💻 **개발 가이드**: [DEVELOPMENT.md](./DEVELOPMENT.md) - 개발/테스트 방법 ⭐ NEW!
- 📦 **실행 파일 빌드**: [BUILD.md](./BUILD.md) - 독립 실행 파일 만들기
- 🔧 **백엔드 상세**: [backend/README.md](./backend/README.md) - API 및 서비스 구조
- 🎨 **프론트엔드 상세**: [frontend/README.md](./frontend/README.md) - UI 컴포넌트 및 구조

---

## 🎯 사용 방식

### 👨‍💻 개발자 (코드 수정)
**빠른 개발 - 빌드 불필요!**

```bash
# 원클릭 실행
dev-run.bat

# 코드 수정 → 저장 → 자동 반영 (핫 리로드)
```

📖 상세 가이드: [DEVELOPMENT.md](./DEVELOPMENT.md)

### 👥 일반 사용자 (배포)
**독립 실행 파일**

```bash
# 배포용 빌드 (최종 단계)
build-scripts\build-all.bat

# 생성된 실행 파일 사용
electron\dist\DocumentAI Setup.exe
```

📖 상세 가이드: [BUILD.md](./BUILD.md)

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

## 🚀 빠른 시작

### 개발자 모드 (권장)

```bash
# 1. 최초 설정 (1회만)
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd ..

cd frontend
npm install
cd ..

# Ollama 설치 및 모델 다운로드
ollama pull mistral

# 2. 개발 서버 실행
dev-run.bat

# 3. 브라우저에서 확인
http://localhost:3000
```

### 배포 빌드 (최종 단계)

```bash
build-scripts\build-all.bat
```

자세한 내용: 
- 개발: [DEVELOPMENT.md](./DEVELOPMENT.md)
- 배포: [BUILD.md](./BUILD.md)

---

## 📝 프로젝트 구조

```
DocumentAI/
├── dev-run.bat             # 개발 서버 시작 ⭐ NEW!
├── dev-stop.bat            # 개발 서버 종료 ⭐ NEW!
├── backend/                # Flask API 서버
│   ├── app/
│   │   ├── main.py        # 진입점
│   │   ├── routers/       # API 라우트
│   │   ├── services/      # 비즈니스 로직
│   │   └── prompt/        # LLM 프롬프트 템플릿
│   └── requirements.txt
├── frontend/              # React 웹 애플리케이션
│   ├── src/
│   └── package.json
├── electron/              # Electron 데스크톱 앱
│   ├── main.js           # Electron 메인 프로세스
│   ├── preload.js        # 보안 브리지
│   └── package.json
├── build-scripts/         # 빌드 스크립트
│   ├── build-all.bat     # Windows 통합 빌드
│   ├── build-all.sh      # Linux/macOS 통합 빌드
│   └── build-backend.spec # PyInstaller 설정
├── DEVELOPMENT.md         # 개발 가이드 ⭐ NEW!
├── BUILD.md              # 빌드 가이드
├── QUICKSTART.md         # 빠른 시작 가이드
└── README.md             # 이 문서
```

---

## 🎯 주요 기능

### 문서 처리
- ✅ PDF 문서 분석 (검색 가능/스캔 문서)
- ✅ 이미지 OCR (Tesseract/EasyOCR)
- ✅ Word 문서 처리 (.docx, .doc)
- ✅ HWP 문서 처리 (pyhwp + fallback)
- ✅ 텍스트 파일 처리 (자동 인코딩 감지)
- ✅ 손글씨 인식 지원
- ✅ 표(Table) 데이터 추출

### AI 분석
- ✅ 로컬 LLM 기반 문서 요약
- ✅ 카테고리별 프롬프트 템플릿
- ✅ 중복 텍스트 제거 및 후처리

### 개발 편의성 (NEW!)
- ✅ **원클릭 개발 서버**: `dev-run.bat`
- ✅ **핫 리로드**: 코드 수정 즉시 반영
- ✅ **빠른 종료**: `dev-stop.bat`
- ✅ **개발 가이드**: DEVELOPMENT.md

### 배포 옵션
- ✅ **독립 실행 파일**: Electron 기반 데스크톱 앱
- ✅ **올인원 패키지**: Python, Node.js 설치 불필요
- ✅ **Ollama 내장**: 로컬 LLM 포함
- ✅ **크로스 플랫폼**: Windows, Linux, macOS

### 기술 특징
- ✅ **외부 프로그램 최소 의존성**
- ✅ **크로스 플랫폼** (Windows, Linux, macOS)
- ✅ **Fallback 메커니즘** (안정성 향상)
- ✅ **빠른 처리 속도** (0.1-3초)

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

## 🔄 최근 업데이트

### v3.1.0 (2024-11-14) - 개발 편의성 대폭 개선 🎉
- ✨ **원클릭 개발 서버**: `dev-run.bat` 추가
- ✨ **개발 서버 종료**: `dev-stop.bat` 추가
- 📚 **개발 가이드 추가**: DEVELOPMENT.md
- 🎯 **개발/배포 명확히 구분**: 워크플로우 개선
- 💡 **빌드 불필요 개발**: 핫 리로드로 빠른 개발

### v3.0.0 (2024-11-14) - Electron 빌드 지원
- ✨ **독립 실행 파일 지원**: Electron 기반 데스크톱 앱
- ✨ **올인원 패키징**: Python, Node.js, Ollama 모두 포함
- ✨ **자동 빌드 스크립트**: 원클릭 빌드 (build-all.bat/sh)
- 📚 **빌드 가이드 추가**: BUILD.md
- 🎯 **일반 사용자 타겟**: 설치 없이 바로 사용 가능

### v2.0.0 (2024-11-11)
- ✨ **HWP 파일 지원 추가** (pyhwp + olefile fallback)
- ✨ **TXT 파일 지원 추가** (자동 인코딩 감지)
- ✨ **Word .doc 파일 개선** (olefile 기반 처리)
- 🚀 **외부 프로그램 의존성 제거** (docx2pdf, pywin32 삭제)
- 🎯 **처리 속도 10배 향상** (python-docx 직접 추출)
- 🛡️ **안정성 향상** (Fallback 메커니즘 추가)

---

## 📊 개발 vs 배포 비교

| 구분 | 개발 모드 | 빌드/배포 |
|------|-----------|-----------|
| **명령어** | `dev-run.bat` | `build-all.bat` |
| **소요 시간** | 3초 | 5-10분 |
| **핫 리로드** | ✅ 지원 | ❌ 없음 |
| **빌드 필요** | ❌ 불필요 | ✅ 필요 |
| **사용 시기** | 코드 개발/테스트 | 최종 배포 |
| **빈도** | 매번 | 배포 시만 |

**핵심: 개발 중에는 빌드하지 마세요!**

---

## ❓ 문제 해결

### 개발 모드 관련
[DEVELOPMENT.md](./DEVELOPMENT.md)의 트러블슈팅 섹션 참고

### 빌드 관련
[BUILD.md](./BUILD.md)의 트러블슈팅 섹션 참고

### 일반 실행 관련
[QUICKSTART.md](./QUICKSTART.md)의 문제 해결 섹션 참고

---

## 📄 라이선스

MIT License

---

## 🤝 기여

이슈 및 Pull Request는 언제나 환영합니다!

---

## 📧 문의

프로젝트 관련 문의사항이 있으시면 Issues를 통해 연락주세요.
