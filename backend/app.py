from flask import Flask, request, jsonify
from flask_cors  import CORS

app = Flask(__name__)
CORS(app)

# 파일 업로드
@app.route('/api/upload', methods=['POST'])
def upload_file():
    
    
    return {"status": "success", "message": "File uploaded successfully"}