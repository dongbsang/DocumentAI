import base64
import mimetypes
import re

from flask import Blueprint, request, jsonify, current_app

from app.services.upload_service import detect_file_format, FileFormat
from app.services.llm_service import analyze_document

upload_bp = Blueprint("upload", __name__)


def extract_json_object(s: str) -> str:
    m = re.search(r'(\{.*\})', s, re.DOTALL)
    return m.group(1) if m else ""


@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    try:
        # 1) 파일 꺼내기 (request.files 또는 data-url)
        if "file" in request.files:
            f = request.files["file"]
            filename = f.filename
            file_bytes = f.read()
        else:
            data_url = request.form.get("file")
            if not data_url or not data_url.startswith("data:"):
                return jsonify({"error": "파일이 없습니다."}), 400

            header, b64 = data_url.split(",", 1)
            file_bytes = base64.b64decode(b64)
            mime = header.split(";")[0].split(":", 1)[1]
            ext = mimetypes.guess_extension(mime) or ""
            filename = f"upload{ext}"

        # 2) 포맷 판별
        fmt_enum = detect_file_format(file_bytes, filename)

        # 지원하지 않는 형식이면 에러
        if fmt_enum == FileFormat.UNKNOWN:
            return jsonify({"error": f"지원하지 않는 파일 형식입니다: {filename}"}), 400

        # Enum.value에서 실제 포맷 문자열 추출
        file_format = fmt_enum.value  # "pdf", "hwp", "word", "image"

        # form 옵션
        category = request.form.get("category", "etc")
        use_handwriting = request.form.get("use_handwriting", "false").lower() == "true"

        # 자동 분석 실행
        summary = analyze_document(
            file_bytes=file_bytes,
            file_format=file_format,
            category=category,
            use_handwriting=use_handwriting
        )

        # 4) 결과 반환
        return jsonify({
            "filename": filename,
            "summary": summary,
            "info": file_format
        }), 200

    except Exception as e:
        current_app.logger.exception("❌ /api/upload 오류")
        return jsonify({
            "error":   "Internal server error",
            "details": str(e)
        }), 500
