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



### 실행방법
✅ 3단계: 동시 실행 (선택사항)
두 개를 한 번에 실행하고 싶다면 다음 중 하나를 선택할 수 있어요:
-----------------------------------
방법 A: VS Code에서 두 개의 터미널로 실행
하나는 backend에서 flask

하나는 frontend에서 npm start
-----------------------------------
방법 B: start-all.sh (bash 스크립트, WSL 또는 Git Bash에서만 가능)
bash

#!/bin/bash
cd backend
venv/Scripts/activate
set FLASK_APP=app.py
set FLASK_ENV=development  # 자동 리로드 + 디버그 모드
flask run
cd ../frontend
npm start
----------------------------------