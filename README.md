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

## 🧠 LLM 모델 설치 가이드 (mistral-7b-instruct-v0.1.Q5_K_M.gguf)
이 프로젝트는 로컬 LLM 모델인 Mistral 7B Instruct (.gguf) 형식의 모델을 사용합니다.
아래 절차를 따라 모델을 다운로드하고, 실행 경로에 배치해 주세요.
📁 1. 모델 저장 디렉토리 준비
mkdir -p backend/app/models
🔗 2. 모델 다운로드
모델 파일은 HuggingFace에서 받을 수 있습니다. 아래 명령어 중 택 1:

✅ 방법 1: git lfs를 사용하는 경우
# Git LFS가 설치되어 있어야 합니다.
git lfs install
git clone https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF
cp Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q5_K_M.gguf backend/app/models/
✅ 방법 2: 직접 다운로드 (wget or 브라우저)

# wget 사용 시
wget -O backend/app/models/mistral-7b-instruct-v0.1.Q5_K_M.gguf \
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q5_K_M.gguf
또는 브라우저에서 아래 링크 접속 후 수동 다운로드:
👉 https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/tree/main

✅ 3. 다운로드 완료 후 디렉토리 확인
최종적으로 다음 경로에 모델이 위치해야 합니다:

backend/
├── app/
│   ├── models/
│   │   └── mistral-7b-instruct-v0.1.Q5_K_M.gguf
⚠️ 주의 사항
해당 모델은 약 4GB 이상이므로 충분한 디스크 용량이 필요합니다.

최초 실행 시 CPU 환경에서는 속도가 다소 느릴 수 있습니다. (GPU 가속은 선택적으로 구성 가능)

------------------------------------------------------------------------------------------------------------------------

🧠 LLM 모델 및 llama-cpp 설치 가이드
이 프로젝트는 문서 AI 파이프라인에서 로컬 LLM (Mistral-7B) 모델을 실행하기 위해 llama-cpp-python 라이브러리를 사용합니다. 아래 절차에 따라 환경을 세팅해 주세요.

📦 1. Python 환경 설정
Python 3.10+ 이상이 권장됩니다.

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install --upgrade pip
🧱 2. llama-cpp-python 설치
llama-cpp-python은 로컬에서 GGUF 포맷 LLM을 실행할 수 있게 해주는 경량 라이브러리입니다.

✅ CMake 기반 수동 설치
cd backend/llama-cpp-python

# CPU 전용 설치
pip install -r requirements.txt
pip install .

# GPU 사용 (CUDA)
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install .
💻 Windows 환경 - Visual Studio C++ 빌드 도구 설치
Windows에서는 C++ 컴파일을 위해 Visual Studio Build Tools가 필요합니다.

🔧 설치 방법:
아래 링크에서 Visual Studio Build Tools 설치:
👉 https://visualstudio.microsoft.com/visual-cpp-build-tools/

설치 시 다음 구성요소를 반드시 체크:
"C++ build tools"
"Windows 10 SDK" 또는 "Windows 11 SDK"
"CMake tools for Windows"
설치 후 재부팅 (필요 시)

📥 3. Mistral 모델 다운로드
프로젝트는 mistral-7b-instruct-v0.1.Q5_K_M.gguf 모델을 사용합니다. Hugging Face에서 수동 다운로드하거나 아래 명령어로 다운로드하세요.

✅ 자동 다운로드 (wget 사용)

mkdir -p backend/app/models

wget -O backend/app/models/mistral-7b-instruct-v0.1.Q5_K_M.gguf \
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q5_K_M.gguf
또는 브라우저에서 직접 다운로드:
👉 https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

🧪 4. 실행 예시 (Python)
from llama_cpp import Llama

llm = Llama(
    model_path="backend/app/models/mistral-7b-instruct-v0.1.Q5_K_M.gguf",
    n_ctx=2048,
    n_gpu_layers=0,  # CPU 환경: 0, GPU 환경: 적절히 조정
    verbose=True
)

response = llm("Q: Hello, who are you?\nA:", max_tokens=100)
print(response)


📌 참고
모델 파일은 4GB 이상이므로 Git에 절대 포함하지 마세요.
GPU 사용을 위해서는 CUDA가 설치된 환경이 필요합니다.
로컬 LLM 실행 시 메모리 요구사항이 높을 수 있습니다 (16GB+ 권장).

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


