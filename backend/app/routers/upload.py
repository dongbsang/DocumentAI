import os
import re
import json
import base64
import mimetypes

from io import BytesIO
from flask import Blueprint, request, jsonify, current_app

from app.services.upload_service import dectect_file_format
# from app.services.ocr_service import extract_text

upload_bp = Blueprint("upload", __name__)

def extract_json_object(s: str) -> str:
    m = re.search(r'(\{.*\})', s, re.DOTALL)
    return m.group(1) if m else ""

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    try:
        # --- 1) 폼 데이터 꺼내기 ---
        # FormData로 올리면 request.files, data-url로 올리면 request.form
        if "file" in request.files:
            f = request.files["file"]
            filename   = f.filename
            file_bytes = f.read()
        else:
            data_url = request.form.get("file")
            if not data_url or not data_url.startswith("data:"):
                return jsonify({"error": "파일이 없습니다."}), 400

            # data:image/pdf;base64,JVBERi0xL...
            header, b64 = data_url.split(",", 1)
            file_bytes = base64.b64decode(b64)
            # MIME 타입 추출
            mime = header.split(";")[0].split(":", 1)[1]
            ext  = mimetypes.guess_extension(mime) or ""
            filename = f"upload{ext}"

        # (카테고리·손글씨 옵션 등이 필요하면 request.form.get 으로 꺼내세요)
        # category  = request.form.get("category")
        # handwrite = request.form.get("handwrite")

        # --- 2) LLM으로 포맷 분류 ---
        fmt_raw = dectect_file_format(file_bytes, filename)
        current_app.logger.info(f"RAW format response: {fmt_raw!r}")
                
        json_str = extract_json_object(fmt_raw)
        if not json_str:
            raise ValueError(f"올바른 JSON이 아닙니다: {fmt_raw}")
        
        current_app.logger.info(f"Extracted JSON: {json_str!r}")
        
        fmt_data = json.loads(json_str)
        file_format = fmt_data.get("format", "unknown")

        # --- 3) 
        # text = extract_text(BytesIO(file_bytes))
        text = ""
        info = file_format

        # 4) 결과 리턴 ---
        return jsonify({
            "filename": filename,
            "ocrResult": {
                "text": text,
                "info": info
            }
        })

    except Exception as e:
        current_app.logger.exception("❌ /api/upload 오류")
        return jsonify({
            "error":   "Internal server error",
            "details": str(e)
        }), 500