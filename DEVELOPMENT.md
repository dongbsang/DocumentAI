# DocumentAI - 개발 가이드

## 🎯 개발 vs 배포

### 개발 모드 (코드 수정 중)
**빌드 불필요! 즉시 실행**

```bash
# 원클릭 실행
dev-run.bat

# 또는 수동 실행
# 터미널 1
cd backend
.venv\Scripts\activate
flask run

# 터미널 2
cd frontend
npm start
```

### 배포 모드 (사용자에게 배포)
**빌드 필요 (5-10분 소요)**

```bash
build-scripts\build-all.bat
```

---

## 🚀 빠른 시작 (개발자용)

### 최초 1회 설정

```bash
# 1. 백엔드 환경 설정
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd ..

# 2. 프론트엔드 환경 설정
cd frontend
npm install
cd ..

# 3. Ollama 설치 및 모델 다운로드
ollama pull mistral
```

### 일상적인 개발

```bash
# 개발 서버 시작 (원클릭)
dev-run.bat

# 코드 수정...
# 저장하면 자동으로 반영됨 (핫 리로드)

# 개발 서버 종료
dev-stop.bat
```

---

## 📂 파일 구조

```
DocumentAI/
├── dev-run.bat          # 개발 서버 시작 (NEW!)
├── dev-stop.bat         # 개발 서버 종료 (NEW!)
├── build-scripts/
│   └── build-all.bat    # 배포용 빌드 (최종 배포 시)
├── backend/
│   └── app/             # 여기서 코드 수정
├── frontend/
│   └── src/             # 여기서 코드 수정
└── electron/            # 빌드 시에만 사용
```

---

## 🔄 개발 워크플로우

### 시나리오 1: 백엔드 코드 수정

```bash
# 1. 개발 서버 실행 (이미 실행 중이면 생략)
dev-run.bat

# 2. backend/app/ 파일 수정
# 예: backend/app/services/pdf_service.py

# 3. 저장하면 Flask가 자동으로 재시작
# 브라우저에서 확인 (http://localhost:3000)

# 4. 만족하면 Git 커밋
git add .
git commit -m "Update PDF service"
```

### 시나리오 2: 프론트엔드 코드 수정

```bash
# 1. 개발 서버 실행 (이미 실행 중이면 생략)
dev-run.bat

# 2. frontend/src/ 파일 수정
# 예: frontend/src/components/FileUpload.js

# 3. 저장하면 React가 자동으로 핫 리로드
# 브라우저가 자동으로 새로고침됨

# 4. 만족하면 Git 커밋
git add .
git commit -m "Update file upload UI"
```

### 시나리오 3: 최종 배포 준비

```bash
# 1. 모든 기능 테스트 완료

# 2. 실행 파일 빌드
build-scripts\build-all.bat

# 3. 생성된 실행 파일 테스트
electron\dist\win-unpacked\DocumentAI.exe

# 4. 문제 없으면 배포
# electron\dist\DocumentAI Setup.exe를 사용자에게 전달
```

---

## 🐛 디버깅 방법

### 백엔드 디버깅

**방법 1: 콘솔 로그**
```python
# backend/app/services/pdf_service.py
print(f"Debug: {variable}")  # 터미널에 출력
```

**방법 2: VSCode 디버거**
1. `.vscode/launch.json` 생성
2. F5로 디버깅 시작
3. 브레이크포인트 설정

**방법 3: Flask 디버그 모드**
```bash
# backend/.env
FLASK_ENV=development  # 이미 설정되어 있음
```

### 프론트엔드 디버깅

**방법 1: 브라우저 개발자 도구**
```javascript
// frontend/src/components/FileUpload.js
console.log('Debug:', data);  // 브라우저 콘솔에 출력
```

**방법 2: React Developer Tools**
- Chrome/Firefox 확장 프로그램 설치
- Components 탭에서 상태 확인

---

## ⚡ 개발 팁

### 빠른 재시작

```bash
# Flask만 재시작 (백엔드 변경 시)
# Backend 터미널에서 Ctrl+C 후
flask run

# React만 재시작 (프론트엔드 변경 시)
# Frontend 터미널에서 Ctrl+C 후
npm start
```

### 포트 충돌 해결

```bash
# 5000 포트 확인
netstat -ano | findstr :5000

# 프로세스 종료
taskkill /PID {프로세스ID} /F

# 또는 자동으로
dev-stop.bat
```

### 캐시 초기화

```bash
# 프론트엔드 캐시
cd frontend
npm cache clean --force
rm -rf node_modules
npm install

# 백엔드 캐시
cd backend
rm -rf __pycache__
```

---

## 🔍 일반적인 개발 순서

```
1. 최초 설정 (1회만)
   └─> 가상환경, 의존성 설치

2. 기능 개발 (반복)
   ├─> dev-run.bat 실행
   ├─> 코드 수정
   ├─> 저장 (자동 반영)
   ├─> 브라우저에서 테스트
   └─> Git 커밋

3. 배포 준비 (최종)
   ├─> 모든 기능 테스트
   ├─> build-scripts\build-all.bat
   └─> 실행 파일 테스트
```

---

## 📊 개발 vs 빌드 비교

| 구분 | 개발 모드 | 빌드 모드 |
|------|-----------|-----------|
| **목적** | 코드 개발/테스트 | 사용자 배포 |
| **실행** | `dev-run.bat` | `build-all.bat` |
| **시간** | 3초 | 5-10분 |
| **핫 리로드** | ✅ 지원 | ❌ 없음 |
| **디버깅** | ✅ 쉬움 | ❌ 어려움 |
| **빌드 필요** | ❌ 불필요 | ✅ 필요 |
| **의존성** | Python, Node 필요 | 독립 실행 |
| **빈도** | 매번 | 배포 시만 |

---

## 🎓 권장 사항

### ✅ 개발 중에는
- `dev-run.bat` 사용
- 코드 수정 후 바로 테스트
- 빌드하지 않고 개발

### ✅ 배포 전에만
- `build-all.bat` 실행
- 실행 파일 생성
- 사용자에게 전달

### ❌ 하지 말아야 할 것
- 코드 수정할 때마다 빌드하지 마세요
- 개발 중에 실행 파일로 테스트하지 마세요
- 빌드 없이 배포하지 마세요

---

## 🆘 문제 해결

### "dev-run.bat를 실행했는데 아무것도 안 돼요"

```bash
# 백엔드 가상환경 확인
cd backend
.venv\Scripts\activate
pip list  # 패키지 확인

# 프론트엔드 의존성 확인
cd frontend
npm list  # 패키지 확인
```

### "코드를 수정했는데 반영이 안 돼요"

- 백엔드: Flask 터미널에서 재시작 메시지 확인
- 프론트엔드: 브라우저 강제 새로고침 (Ctrl+Shift+R)
- 캐시 문제: `dev-stop.bat` 후 재시작

### "포트가 이미 사용 중이에요"

```bash
# 모든 개발 서버 종료
dev-stop.bat

# 다시 시작
dev-run.bat
```

---

## 📝 요약

```
개발 중: dev-run.bat → 코드 수정 → 자동 반영 → 테스트 → 커밋
                     (빌드 불필요!)

배포 시: build-all.bat → 실행 파일 생성 → 테스트 → 배포
                     (최종 단계만!)
```

**핵심: 개발 중에는 절대 빌드하지 마세요! 시간 낭비입니다.** 🚀
