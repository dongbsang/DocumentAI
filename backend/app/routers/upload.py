import base64
import mimetypes
import re
import json

from flask import Blueprint, request, jsonify, current_app

from app.services.upload_service import detect_file_format, FileFormat
from app.services.llm_service import analyze_document
import logging

upload_bp = Blueprint("upload", __name__)

# 로거 설정
logger = logging.getLogger(__name__)


def extract_json_from_text(text: str) -> str:
    """
    텍스트에서 JSON 부분만 추출
    
    Args:
        text: 원본 텍스트 (LLM 응답)
    
    Returns:
        str: JSON 문자열
    """
    logger.info("=" * 80)
    logger.info("📤 extract_json_from_text 시작")
    logger.info(f"📏 입력 텍스트 길이: {len(text)} 자")
    logger.info(f"📝 입력 텍스트 샘플 (처음 200자):\n{text[:200]}")
    logger.info("=" * 80)
    
    # 1. ```json ... ``` 마크다운 제거
    markdown_pattern = r'```json\s*(.*?)\s*```'
    markdown_match = re.search(markdown_pattern, text, re.DOTALL)
    if markdown_match:
        result = markdown_match.group(1).strip()
        logger.info("✅ JSON 마크다운 블록 발견")
        logger.info(f"📏 추출된 JSON 길이: {len(result)} 자")
        return result
    
    # 2. ``` ... ``` 제거
    code_pattern = r'```\s*(.*?)\s*```'
    code_match = re.search(code_pattern, text, re.DOTALL)
    if code_match:
        result = code_match.group(1).strip()
        logger.info("✅ 코드 블록 발견")
        logger.info(f"📏 추출된 JSON 길이: {len(result)} 자")
        return result
    
    # 3. { ... } JSON 객체 찾기
    json_pattern = r'\{.*\}'
    json_match = re.search(json_pattern, text, re.DOTALL)
    if json_match:
        result = json_match.group(0)
        logger.info("✅ JSON 객체 발견")
        logger.info(f"📏 추출된 JSON 길이: {len(result)} 자")
        return result
    
    # 4. 찾지 못하면 원본 반환
    logger.warning("⚠️ JSON 패턴을 찾지 못함, 원본 텍스트 반환")
    return text


def parse_llm_response(llm_response: str, category: str, filename: str, file_format: str) -> dict:
    """
    LLM 응답을 구조화된 JSON으로 파싱
    
    Args:
        llm_response: LLM이 반환한 원본 텍스트
        category: 문서 카테고리
        filename: 파일명
        file_format: 파일 형식
    
    Returns:
        dict: 구조화된 응답
    """
    try:
        logger.info("=" * 80)
        logger.info("📤 parse_llm_response 시작")
        logger.info(f"📏 LLM 응답 길이: {len(llm_response)} 자")
        logger.info(f"📝 LLM 응답 샘플 (처음 300자):\n{llm_response[:300]}")
        logger.info("=" * 80)
        
        # ✅ 빈 응답 체크
        if not llm_response or not llm_response.strip():
            logger.error("❌ LLM 응답이 비어있습니다!")
            return create_fallback_response("", category, filename, file_format)
        
        # 1. JSON 추출
        json_str = extract_json_from_text(llm_response)
        logger.info(f"📝 추출된 JSON 길이: {len(json_str)} 자")
        logger.info(f"📝 추출된 JSON 샘플 (처음 300자):\n{json_str[:300]}")
        
        # 2. JSON 파싱
        try:
            parsed_data = json.loads(json_str)
            logger.info(f"✅ JSON 파싱 성공")
            logger.info(f"📋 파싱된 데이터 키: {list(parsed_data.keys())}")
        except json.JSONDecodeError as parse_error:
            logger.error(f"❌ JSON 파싱 실패: {parse_error}")
            logger.error(f"❌ 파싱 시도한 JSON (처음 500자):\n{json_str[:500]}")
            logger.error(f"❌ 파싱 시도한 JSON (전체):\n{json_str}")
            raise
        
        # 3. 구조 검증 (summary, details 필드가 있는지)
        if "summary" not in parsed_data:
            logger.warning("⚠️ 'summary' 필드 없음, 폴백 사용")
            return create_fallback_response(llm_response, category, filename, file_format)
        
        if "details" not in parsed_data:
            logger.warning("⚠️ 'details' 필드 없음, 폴백 사용")
            return create_fallback_response(llm_response, category, filename, file_format)
        
        # 4. 공통 구조로 래핑
        structured_response = {
            "success": True,
            "doc_type": category,
            "file_name": filename,
            "extracted_format": file_format,
            "data": parsed_data
        }
        
        logger.info(f"✅ 구조화된 응답 생성 완료 (카테고리: {category})")
        logger.info(f"📋 최종 응답 키: {list(structured_response.keys())}")
        logger.info(f"📋 data 키: {list(structured_response['data'].keys())}")
        return structured_response
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON 파싱 실패: {e}")
        logger.error(f"문제가 된 텍스트 (처음 500자):\n{json_str[:500] if 'json_str' in locals() else llm_response[:500]}")
        return create_fallback_response(llm_response, category, filename, file_format)
    
    except Exception as e:
        logger.error(f"❌ 응답 파싱 오류: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return create_fallback_response(llm_response, category, filename, file_format)


def create_fallback_response(raw_text: str, category: str, filename: str, file_format: str) -> dict:
    """
    파싱 실패 시 폴백 응답 생성
    
    Args:
        raw_text: LLM 원본 응답
        category: 문서 카테고리
        filename: 파일명
        file_format: 파일 형식
    
    Returns:
        dict: 폴백 응답 구조
    """
    logger.warning("⚠️ JSON 파싱 실패, 폴백 응답 생성")
    
    # 카테고리별 기본 제목
    category_titles = {
        "receipt": "영수증 분석 결과",
        "resume": "이력서 분석 결과",
        "diagnosis": "진단서 분석 결과",
        "etc": "문서 분석 결과"
    }
    
    return {
        "success": False,
        "doc_type": category,
        "file_name": filename,
        "extracted_format": file_format,
        "data": {
            "summary": {
                "title": category_titles.get(category, "문서 분석 결과"),
                "subtitle": f"{filename}",
                "datetime": None,
                "description": "구조화된 JSON 파싱 실패, 원문을 확인하세요",
                "status": {
                    "label": "파싱 오류",
                    "type": "warning"
                }
            },
            "details": {
                "raw_content": raw_text[:1000] if len(raw_text) > 1000 else raw_text,
                "note": "LLM이 올바른 JSON 형식으로 응답하지 않았습니다."
            },
            "meta": {
                "error": "JSON 파싱 실패",
                "original_length": len(raw_text),
                "parsing_attempted": True
            }
        }
    }


@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    try:
        logger.info("=" * 80)
        logger.info("📤 /upload 엔드포인트 호출됨")
        logger.info("=" * 80)
        
        # 1) 파일 꺼내기 (request.files 또는 data-url)
        if "file" in request.files:
            f = request.files["file"]
            filename = f.filename
            file_bytes = f.read()
            logger.info(f"📁 파일 업로드 (multipart): {filename}")
        else:
            data_url = request.form.get("file")
            if not data_url or not data_url.startswith("data:"):
                logger.error("❌ 파일이 없습니다.")
                return jsonify({"error": "파일이 없습니다."}), 400

            header, b64 = data_url.split(",", 1)
            file_bytes = base64.b64decode(b64)
            mime = header.split(";")[0].split(":", 1)[1]
            ext = mimetypes.guess_extension(mime) or ""
            filename = f"upload{ext}"
            logger.info(f"📁 파일 업로드 (data URL): {filename}")

        logger.info(f"📏 파일 크기: {len(file_bytes)} bytes")

        # 2) 포맷 판별
        fmt_enum = detect_file_format(file_bytes, filename)

        # 지원하지 않는 형식이면 에러
        if fmt_enum == FileFormat.UNKNOWN:
            logger.error(f"❌ 지원하지 않는 파일 형식: {filename}")
            return jsonify({"error": f"지원하지 않는 파일 형식입니다: {filename}"}), 400

        # Enum.value에서 실제 포맷 문자열 추출
        file_format = fmt_enum.value  # "pdf", "hwp", "word", "image"

        # form 옵션
        category = request.form.get("category", "etc")
        use_handwriting = request.form.get("use_handwriting", "false").lower() == "true"

        logger.info(f"📋 카테고리: {category}, 손글씨: {use_handwriting}, 포맷: {file_format}")

        # 3) 자동 분석 실행
        logger.info("🤖 LLM 분석 시작...")
        raw_response = analyze_document(
            file_bytes=file_bytes,
            file_format=file_format,
            category=category,
            use_handwriting=use_handwriting
        )
        
        logger.info("=" * 80)
        logger.info(f"✅ LLM 분석 완료")
        logger.info(f"📏 응답 길이: {len(raw_response)} 자")
        logger.info(f"📝 응답 샘플 (처음 300자):\n{raw_response[:300]}")
        logger.info("=" * 80)

        # 4) 응답 파싱 및 구조화
        structured_response = parse_llm_response(
            llm_response=raw_response,
            category=category,
            filename=filename,
            file_format=file_format
        )

        # 5) 디버그 로그
        logger.info("=" * 80)
        logger.info("📤 최종 응답 구조:")
        logger.info(f"  - success: {structured_response.get('success')}")
        logger.info(f"  - doc_type: {structured_response.get('doc_type')}")
        logger.info(f"  - file_name: {structured_response.get('file_name')}")
        if structured_response.get('data'):
            logger.info(f"  - data.summary.title: {structured_response.get('data', {}).get('summary', {}).get('title')}")
        logger.info("=" * 80)

        # 6) 구조화된 응답 반환
        return jsonify(structured_response), 200

    except Exception as e:
        current_app.logger.exception("❌ /api/upload 오류")
        logger.error("=" * 80)
        logger.error(f"❌ /api/upload 오류: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        logger.error("=" * 80)
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "details": str(e)
        }), 500
