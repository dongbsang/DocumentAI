import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드 (backend 디렉토리의 .env)
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

from flask import Flask
from flask_cors import CORS

# Routers
from app.routers.status import status_bp
from app.routers.upload import upload_bp

def create_app():
    app = Flask(__name__, root_path=os.path.dirname(__file__))
    
    # CORS 설정 - 모든 출처 허용 (개발 환경)
    CORS(app, 
         origins="*",
         methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
         allow_headers=["Content-Type", "Authorization"],
         supports_credentials=False)

    # Blueprint 등록
    app.register_blueprint(status_bp, url_prefix="/api")
    app.register_blueprint(upload_bp, url_prefix="/api")
    
    # 로깅 설정
    if app.config.get('ENV') == 'development':
        app.logger.setLevel('DEBUG')
    
    return app
