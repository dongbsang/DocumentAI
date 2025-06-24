
# 1. 도구, url 세팅
1) cp .env.example .env 을 진행
2) .env > OPEN_API_KEY에 GPT KEY값을 넣는다.
3) 

# 2. 가상환경 생성 & 활성화
1) 백엔드 디렉토리에서
python -m venv .venv
2) macOS / WSL / Git Bash
source .venv/bin/activate
3) Windows PowerShell
.\.venv\Scripts\Activate

# 3. 백엔드 실행
cd backend

1) 의존성 설치
    pip install -r requirements.txt

2) .env 로드 확인 (예: python-dotenv 사용)
    load_dotenv() 코드가 백엔드 진입점(app.py 등)에 있어야 합니다.

3) 서버 실행
 Flask 프로젝트라면:
export FLASK_APP=app.py        # Windows CMD: set FLASK_APP=app.py
export FLASK_ENV=development   # (선택) 디버그 모드 활성화
flask run

4) 실행 방법
 - FastAPI(Uvicorn)라면:
   uvicorn main:app --reload
 - Django라면:
   python manage.py runserver