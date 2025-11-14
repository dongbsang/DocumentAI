# DocumentAI - Electron 데스크톱 앱 빌드 가이드

이 가이드는 DocumentAI를 **독립 실행 파일(.exe)**로 빌드하는 방법을 안내합니다.

---

## 🎯 빌드 결과물

사용자는 다음 중 하나를 사용할 수 있습니다:

1. **설치 프로그램** (`DocumentAI Setup.exe`)
   - 일반적인 소프트웨어처럼 설치
   - 시작 메뉴 및 바탕화면 바로가기 생성
   - 자동 업데이트 지원 가능

2. **포터블 버전** (`win-unpacked/DocumentAI.exe`)
   - 설치 없이 바로 실행
   - USB나 다른 폴더로 이동 가능
   - 관리자 권한 불필요

---

## 📋 빌드 전 준비사항

### 1. Node.js 설치
```bash
# Node.js 16 이상 필요
node --version
npm --version
```

### 2. Python 환경 설정
```bash
# Python 3.10 이상 필요
python --version

# 백엔드 가상환경 활성화
cd backend
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# hwp5 설치 (pyhwp 대신)
pip install -r requirements.txt
```

### 3. PyInstaller 설치
```bash
pip install pyinstaller
```

### 4. LibreOffice Portable 준비 ⭐ NEW!

**HWP → PDF 변환 기능을 위해 필수**

#### Windows
1. https://www.libreoffice.org/download/portable-versions/ 접속
2. **LibreOffice Portable** 다운로드 (약 300MB)
3. 다운로드한 파일 실행하여 압축 해제
4. 프로젝트 루트에 복사:

```
D:\AI\DocumentAI\libreoffice\
├── program\
│   ├── soffice.exe    ← 이 파일이 있어야 함
│   └── ...
└── ...
```

**확인 방법:**
```bash
# 이 파일이 존재해야 함
D:\AI\DocumentAI\libreoffice\program\soffice.exe
```

#### Linux/macOS
```bash
# 시스템에 LibreOffice 설치
# Ubuntu/Debian
sudo apt-get install libreoffice

# macOS
brew install libreoffice
```

### 5. Ollama 준비 (선택)

```bash
# Ollama 설치: https://ollama.com/download

# 프로젝트 루트에 ollama 디렉토리 생성
mkdir ollama

# Ollama 실행 파일 복사
# Windows: ollama.exe를 ollama/ 폴더에 복사
# Linux/macOS: ollama 바이너리를 ollama/ 폴더에 복사

# Mistral 모델 다운로드
ollama pull mistral

# 모델 파일을 ollama/models/ 로 복사
# Windows: C:\Users\{username}\.ollama\models -> ollama\models
# Linux/macOS: ~/.ollama/models -> ollama/models
```

**중요**: Ollama와 모델 파일을 프로젝트에 포함하면 최종 실행 파일이 4-5GB가 됩니다.

---

## 🚀 빌드 방법

### Windows

#### 자동 빌드 (권장)
```bash
# 프로젝트 루트에서 실행
build-scripts\build-all.bat
```

**빌드 과정:**
1. ✅ 프론트엔드 빌드
2. ✅ 백엔드 PyInstaller 빌드
3. ⚠️ LibreOffice Portable 준비 확인 (없으면 대기)
4. ⚠️ Ollama 준비 확인 (선택사항)
5. ✅ Electron 의존성 설치
6. ✅ Electron 앱 빌드
7. ✅ LibreOffice를 빌드 출력에 복사

#### 수동 빌드
```bash
# 1. 프론트엔드 빌드
cd frontend
npm install
npm run build
cd ..

# 2. 백엔드 빌드
cd backend
.venv\Scripts\activate
pyinstaller ..\build-scripts\build-backend.spec
cd ..

# 3. LibreOffice 준비 (위 Step 4 참고)

# 4. Electron 빌드
cd electron
npm install
npm run build:win
cd ..

# 5. LibreOffice 복사
xcopy /E /I /Y libreoffice electron\dist\win-unpacked\libreoffice
```

### Linux / macOS

#### 자동 빌드 (권장)
```bash
# 실행 권한 부여
chmod +x build-scripts/build-all.sh

# 빌드 실행
./build-scripts/build-all.sh
```

---

## 📂 빌드 결과물 위치

```
electron/dist/
├── DocumentAI Setup.exe       # 설치 프로그램 (Windows)
├── DocumentAI-1.0.0.exe       # NSIS 설치 파일
├── win-unpacked/              # 포터블 버전
│   ├── DocumentAI.exe         # 바로 실행 가능
│   ├── resources/
│   │   ├── backend.exe        # Flask 서버
│   │   └── ...
│   ├── libreoffice/           # LibreOffice Portable ⭐
│   │   └── program/
│   │       └── soffice.exe
│   └── ollama/                # Ollama (선택)
└── ...
```

**파일 크기 예상:**
- LibreOffice 미포함: ~200MB
- LibreOffice 포함: ~700MB
- Ollama 포함: ~5GB

---

## ⚙️ 빌드 커스터마이징

### 앱 아이콘 변경

1. 아이콘 파일 준비 (256x256 PNG 또는 ICO)
2. `electron/icon.ico` (Windows) 또는 `electron/icon.png` (Linux/macOS) 로 저장
3. `electron/package.json` 확인:
```json
{
  "build": {
    "win": {
      "icon": "icon.ico"
    }
  }
}
```

### 앱 버전 변경

`electron/package.json` 수정:
```json
{
  "version": "1.0.0"  // 원하는 버전으로 변경
}
```

### 설치 프로그램 옵션 변경

`electron/package.json`의 `build.nsis` 섹션 수정:
```json
{
  "build": {
    "nsis": {
      "oneClick": false,                    // 사용자 정의 설치 허용
      "allowToChangeInstallationDirectory": true,
      "createDesktopShortcut": true,        // 바탕화면 바로가기
      "createStartMenuShortcut": true       // 시작 메뉴 바로가기
    }
  }
}
```

---

## 🔍 트러블슈팅

### 문제 1: PyInstaller 빌드 오류
```
ModuleNotFoundError: No module named 'xxx'
```

**해결책**: `build-scripts/build-backend.spec`의 `hiddenimports`에 모듈 추가
```python
hiddenimports=[
    'xxx',  # 누락된 모듈 추가
],
```

### 문제 2: Electron 빌드 오류
```
Error: Cannot find module 'xxx'
```

**해결책**:
```bash
cd electron
npm install
```

### 문제 3: LibreOffice를 찾을 수 없음

**증상**: 빌드 후 HWP 파일 처리 시 "LibreOffice를 찾을 수 없습니다" 오류

**해결책**:
1. `libreoffice/program/soffice.exe` 파일 존재 확인
2. 빌드 스크립트가 제대로 복사했는지 확인:
```bash
dir electron\dist\win-unpacked\libreoffice\program\soffice.exe
```

### 문제 4: 백엔드 실행 파일이 시작되지 않음

**해결**: `build-backend.spec`에서 `console=True`로 설정하여 에러 로그 확인
```python
exe = EXE(
    ...
    console=True,  # False → True로 변경
)
```

### 문제 5: hwp5 설치 오류

**증상**: `pip install hwp5` 실패

**해결책**:
```bash
# requirements.txt에서 버전 확인
pip install hwp5==0.1.3

# 또는 최신 버전 시도
pip install hwp5
```

---

## 📦 배포 전 체크리스트

- [ ] 모든 기능이 정상 작동하는지 테스트
- [ ] 프론트엔드 빌드 완료 (`frontend/build/` 존재)
- [ ] 백엔드 빌드 완료 (`backend/dist/backend.exe` 존재)
- [ ] LibreOffice Portable 준비 완료 (`libreoffice/program/soffice.exe` 존재) ⭐
- [ ] HWP → PDF 변환 테스트 완료
- [ ] Ollama 및 모델 준비 완료 (선택, `ollama/ollama.exe`, `ollama/models/` 존재)
- [ ] Electron 빌드 성공 (`electron/dist/` 존재)
- [ ] 포터블 버전 실행 테스트
- [ ] 설치 프로그램 테스트

---

## 🎉 배포

빌드가 완료되면:

1. **설치 프로그램 배포**
   - `electron/dist/DocumentAI Setup.exe`를 사용자에게 전달
   - 다운로드 링크 제공 (Google Drive, GitHub Releases 등)

2. **포터블 버전 배포**
   - `electron/dist/win-unpacked/` 폴더 전체를 ZIP으로 압축
   - 압축 파일을 사용자에게 전달

---

## 🔄 자동 업데이트 (선택사항)

자동 업데이트를 원한다면:

1. `electron-updater` 설정
2. 업데이트 서버 구축 (예: GitHub Releases)
3. `electron/main.js`에 업데이트 체크 로직 추가

자세한 내용은 [electron-updater 문서](https://www.electron.build/auto-update) 참고

---

## 💡 최적화 팁

### 빌드 크기 줄이기

1. **Ollama 제외**: 사용자가 Ollama를 별도 설치하도록 안내
2. **LibreOffice Portable 제외**: 사용자가 LibreOffice를 시스템에 설치하도록 안내 (권장하지 않음)
3. **불필요한 의존성 제거**: `excludes`에 추가

### 빌드 속도 향상

1. **캐시 활용**: 변경되지 않은 부분은 재빌드 생략
2. **병렬 빌드**: 프론트엔드와 백엔드를 동시에 빌드
3. **클라우드 빌드**: CI/CD 파이프라인 사용 (GitHub Actions 등)

---

## 📊 빌드 결과 비교

| 구성 | 크기 | 사용자 설치 필요 | HWP → PDF |
|------|------|-----------------|-----------|
| **기본** | ~200MB | ❌ 없음 | ❌ 불가 |
| **+ LibreOffice** | ~700MB | ❌ 없음 | ✅ 가능 ⭐ |
| **+ Ollama** | ~5GB | ❌ 없음 | ✅ 가능 |

**권장**: LibreOffice 포함 빌드 (~700MB)

---

## 📞 도움말

문제가 발생하면:
1. 빌드 로그 확인
2. `electron/main.js`에서 console.log 확인
3. Issues에 문의

---

**끝! 성공적인 빌드를 기원합니다! 🎊**
