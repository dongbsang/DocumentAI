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

------------------------------------------------------------------------------------------------------------------------

### 최초 해야하는 것
 .env.example 파일을 복사해서 .env 파일로 만듭니다
  1) cp .env.example .env
  2) .env 에서 필요한 환경변수를 정의합니다
  3) 보안을 위해 민감정보는 .env 에만 저장
  4) (추후) OPENAI_API_KEY 제거 예정

------------------------------------------------------------------------------------------------------------------------

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

------------------------------------------------------------------------------------------------------------------------

🧠 LLM 모델 및 Ollama 설치 가이드
이 프로젝트는 문서 AI 파이프라인에서 로컬 LLM(Mistral-7B) 모델을 실행하기 위해 Ollama를 사용합니다.
Ollama는 간편하게 로컬 LLM을 다운로드 및 실행할 수 있는 통합 플랫폼입니다.

아래 절차에 따라 환경을 세팅해 주세요.

📦 1. Python 환경 설정
Python 3.10+ 이상이 권장됩니다.

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install --upgrade pip

🔧 2. Ollama 설치
운영체제에 따라 아래 방식으로 설치합니다:

✅ Windows
아래 링크에서 .msi 설치 파일 다운로드
👉 https://ollama.com/download
실행 후 설치 및 재부팅

✅ macOS
brew install ollama

✅ Linux (Ubuntu/Debian)
curl -fsSL https://ollama.com/install.sh | sh

설치 확인:
ollama --version

📥 3. Mistral 모델 다운로드 및 실행
ollama run mistral
최초 실행 시 모델이 자동 다운로드됩니다.
이후에는 로컬에서 빠르게 재사용됩니다.

설치된 모델 목록 확인:
ollama list

모델 삭제:
ollama remove mistral

🧪 4. 실행 예시 (Python - LangChain 연동)
from langchain_community.llms import Ollama
llm = Ollama(model="mistral")  # 설치된 모델명

response = llm.invoke("Q: Hello, who are you?\nA:")
print(response)
LangChain에서 Ollama 클래스를 통해 LLM을 바로 호출할 수 있습니다.

🧠 지원되는 기타 모델들
모델 이름	실행 명령어
LLaMA 3	ollama run llama3
Code Llama	ollama run codellama
Phi-3	ollama run phi3
Gemma	ollama run gemma
Dolphin-mixtral	ollama run dolphin-mixtral

📌 참고 사항
Ollama는 CPU 및 GPU를 자동 감지하여 사용합니다.
모델 파일은 대용량(4~8GB)이므로 Git에 포함하지 마세요.
메모리 최소 요구사항: RAM 16GB 이상 권장
Ollama는 내부적으로 API 서버(localhost:11434)를 실행합니다.

------------------------------------------------------------------------------

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


