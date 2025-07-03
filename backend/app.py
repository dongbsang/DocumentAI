import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from io import BytesIO

# 로컬 패키지 모듈 임포트
from service.ocr import extract_text
from utils.openai_utils import process_vision_stream

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"]) # 리액트 앱의 CORS 설정

@app.route('/api/upload', methods=['POST'])
def upload_file():
    
    uploaded = request.files.get("file")
    if not uploaded:
        return jsonify({"error": "No file part"}), 400

    # 파일명만 추출
    filename = uploaded.filename
    # OCR 결과에 대한 처리
    ocr_result = "미구현 상태"

    # 원하는 키로 JSON 응답
    return jsonify({
        "filename": filename,
        "ocr_result": ocr_result
    })

    '''
    # 업로드 파일 존재 여부 확인
    if not uploaded:
        return jsonify({"error": "No file part"}), 400
    
    # 파일 내용 읽기
    file_bytes = uploaded.read()
    
    # 1) TEXT OCR 
    text = extract_text(BytesIO(file_bytes))
    
    # 2) GPT Vision으로 정보 추출
    info = process_vision_stream(BytesIO(file_bytes))
    
    return jsonify({
        "text": text,   # OCR로 추출된 텍스트
        "info": info    # GPT Vision으로 추출된 정보
    })  
    '''
if __name__ == '__main__':
    # 디버그 모드로 개발 서버 실행
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    