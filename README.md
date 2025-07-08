### 구조설계

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


### 최초 해야하는 것
 .env.example 파일을 복사해서 .env 파일로 만듭니다
  1) cp .env.example .env
  2) .env 에서 필요한 환경변수를 정의합니다
  3) 보안을 위해 민감정보는 .env 에만 저장
  4) (추후) OPENAI_API_KEY 제거 예정


## 🚀 개발 환경(환경 구성) 설정
프로젝트를 실행하기 전에 독립된 Python 환경을 만들고, 필요한 패키지를 한 번에 설치하세요.
### 1. 가상환경 생성하기
cd backend
python -m venv .venv
### 2. 가상환경 활성화
.\.venv\Scripts\Activate.ps1
### 3. 필수 라이브러리 설치하기
pip install -r requirements.txt
1) flask 사용 시 import flask 오류 없이 동작
2) openai 클라이언트 사용 시 import openai 오류 없이 동작
### 4. 가상환경 나가기
deactivate


### 실행방법
✅ 3단계: 동시 실행 (선택사항)
두 개를 한 번에 실행하고 싶다면 다음 중 하나를 선택할 수 있어요:
-----------------------------------
방법 A: VS Code에서 두 개의 터미널로 실행
하나는 backend에서 flask run

하나는 frontend에서 npm start
-----------------------------------
방법 B: start-all.sh (bash 스크립트, WSL 또는 Git Bash에서만 가능)
bash

'샵'!/bin/bash
(최초만) python -m venv .venv
.venv/Scripts/activate
cd backend
set FLASK_APP=app.py
set FLASK_ENV=development  // 자동 리로드 + 디버그 모드
flask run
cd ../frontend
npm start
----------------------------------