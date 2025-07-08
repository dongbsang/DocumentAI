import os
from dotenv import load_dotenv
load_dotenv()   

from flask import Flask
from flask_cors import CORS

# Routers
from app.routers.status import status_bp
from app.routers.upload import upload_bp

def create_app():
    app = Flask(__name__, root_path=os.path.dirname(__file__))
    # React dev-server 허용
    CORS(app, origins=["http://localhost:3000"])

    # Blueprint 등록 (prefix 로 묶기)
    app.register_blueprint(status_bp, url_prefix="/api")
    app.register_blueprint(upload_bp, url_prefix="/api")

    return app