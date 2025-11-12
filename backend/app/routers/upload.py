import base64
import mimetypes
import re
import json
import logging

from flask import Blueprint, request, current_app

from app.services.upload_service import detect_file_format, FileFormat
from app.services.llm_service import analyze_document
from app.models.response import ErrorCode
from app.utils.response_utils import create_success_response, create_error_response

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
    logger.info("=" * 80)
    
    # 1. ```json ... ``` 마크다운 제거
    markdown_pattern = r'```json\s*(.*?)\s*```'
    markdown_match = re.search(markdown_pattern, text, re.DOTALL)
    if markdown_match:
        result = markdown_match.group(1).strip()
        logger.info("✅ JSON 마크다운 블록 발견")
        return result
    
    # 2. ``` ... ``` 제거
    code_pattern = r'```\s*(.*?)\s*```'
    code_match = re.search(code_pattern, text, re.DOTALL)
    if code_match:
        result = code_match.group(1).strip()
        logger.info("✅ 코드 블록 발견")
        return result
    
    # 3. { ... } JSON 객체 찾기
    json_pattern = r'\{.*\}'
    json_match = re.search(json_pattern, text, re.DOTALL)
    if json_match:
        result = json_match.group(0)
        logger.info("✅ JSON 객체 발견")
        return result
    
    # 4. 찾지 못하면 원본 반환
    logger.warning("⚠️ JSON 패턴을 찾지 못함, 원본 텍스트 반환")
    return text


def validate_receipt_amounts(parsed_data: dict, category: str) -> dict:
    """
    영수증 금액 데이터 검증
    - 예시 금액(464718, 350000, 12300, 89000, 256700 등) 감지 및 경고
    
    Args:
        parsed_data: 파싱된 JSON 데이터
        category: 문서 카테고리
    
    Returns:
        dict: 검증된 데이터 (메타에 경고 추가)
    """
    if category != "receipt":
        return parsed_data
    
    try:
        # 프롬프트 예시에 사용된 의심스러운 금액들
        suspicious_amounts = [
            464718,  # 기존 네이버페이 예시
            350000,  # 기존 주식회사 은다 예시
            12300,   # 새 예시 1
            89000,   # 새 예시 2
            256700,  # 새 예시 3
            14000,   # 기존 스타벅스 예시 (삭제됨)
        ]
        
        payment = parsed_data.get("details", {}).get("payment", {})
        amount_total = payment.get("amount_total")
        
        if amount_total in suspicious_amounts:
            logger.warning(f"⚠️ 의심스러운 예시 금액 감지: {amount_total}원")
            logger.warning("   이 금액이 프롬프트 예시와 일치합니다. 실제 문서 금액인지 확인 필요.")
            
            # 메타 정보에 경고 추가
            if "meta" not in parsed_data:
                parsed_data["meta"] = {}
            
            parsed_data["meta"]["amount_warning"] = True
            parsed_data["meta"]["amount_warning_message"] = "프롬프트 예시와 동일한 금액이 감지되었습니다."
        
        return parsed_data
        
    except Exception as e:
        logger.error(f"❌ 금액 검증 중 오류: {e}")
        return parsed_data


def clean_receipt_items(parsed_data: dict, category: str) -> dict:
    """
    영수증 품목 데이터 정제
    - 예시 데이터(STAY3 등) 필터링
    - 빈 품목 처리
    
    Args:
        parsed_data: 파싱된 JSON 데이터
        category: 문서 카테고리
    
    Returns:
        dict: 정제된 데이터
    """
    if category != "receipt":
        return parsed_data
    
    try:
        details = parsed_data.get("details", {})
        items = details.get("items", [])
        
        if not items or not isinstance(items, list):
            logger.info("📦 품목 없음, 빈 배열 유지")
            return parsed_data
        
        # 예시 데이터 필터링 (프롬프트의 예시 품목명들)
        suspicious_names = [
            "STAY3",
            "아메리카노",
            "카페라떼",
            "카라멜마끼아또",
            "치즈케이크",
            "무선청소기"
        ]
        filtered_items = []
        
        for item in items:
            item_name = item.get("name", "")
            
            # 예시 데이터 감지
            if item_name in suspicious_names:
                logger.warning(f"⚠️ 예시 데이터 감지: '{item_name}' - 제거")
                continue
            
            filtered_items.append(item)
        
        # 필터링 결과 적용
        if len(filtered_items) != len(items):
            logger.info(f"✅ 품목 필터링: {len(items)}개 → {len(filtered_items)}개")
            details["items"] = filtered_items
        
        return parsed_data
        
    except Exception as e:
        logger.error(f"❌ 품목 정제 중 오류: {e}")
        return parsed_data


def parse_llm_response(
    llm_response: str,
    category: str,
    filename: str,
    file_format: str
) -> dict:
    """
    LLM 응답을 구조화된 데이터로 파싱
    ✅ 기존 프론트엔드 컴포넌트와 호환되는 구조 유지
    
    Args:
        llm_response: LLM이 반환한 원본 텍스트
        category: 문서 카테고리
        filename: 파일명
        file_format: 파일 형식
    
    Returns:
        dict: 구조화된 응답
        
    Raises:
        ValueError: JSON 파싱 실패 시
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
            raise ValueError("LLM 응답이 비어있습니다")
        
        # 1. JSON 추출
        json_str = extract_json_from_text(llm_response)
        logger.info(f"📝 추출된 JSON 길이: {len(json_str)} 자")
        
        # 2. JSON 파싱
        try:
            parsed_data = json.loads(json_str)
            logger.info(f"✅ JSON 파싱 성공")
            logger.info(f"📋 파싱된 데이터 키: {list(parsed_data.keys())}")
        except json.JSONDecodeError as parse_error:
            logger.error(f"❌ JSON 파싱 실패: {parse_error}")
            logger.error(f"❌ 파싱 시도한 JSON (처음 500자):\n{json_str[:500]}")
            raise ValueError(f"JSON 파싱 실패: {str(parse_error)}")
        
        # 3. 구조 검증 (summary, details 필드가 있는지)
        if "summary" not in parsed_data:
            logger.warning("⚠️ 'summary' 필드 없음")
            raise ValueError("'summary' 필드가 없습니다")
        
        if "details" not in parsed_data:
            logger.warning("⚠️ 'details' 필드 없음")
            raise ValueError("'details' 필드가 없습니다")
        
        # 3.5. 영수증 데이터 정제 및 검증
        parsed_data = validate_receipt_amounts(parsed_data, category)  # 금액 검증
        parsed_data = clean_receipt_items(parsed_data, category)       # 품목 정제
        
        # ✅ 4. 기존 프론트엔드 구조와 호환되도록 변환
        structured_response = {
            "file_name": filename,
            "doc_type": category,
            "extracted_format": file_format,
            "summary": parsed_data.get("summary", {}),
            "details": parsed_data.get("details", {}),
            "meta": parsed_data.get("meta", {})
        }
        
        logger.info(f"✅ 구조화된 응답 생성 완료 (카테고리: {category})")
        logger.info(f"📋 최종 응답 키: {list(structured_response.keys())}")
        return structured_response
        
    except Exception as e:
        logger.error(f"❌ 응답 파싱 오류: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


def create_fallback_data(
    raw_text: str,
    category: str,
    filename: str,
    file_format: str
) -> dict:
    """
    파싱 실패 시 폴백 응답 생성
    ✅ 기존 프론트엔드 구조와 호환
    
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
        "file_name": filename,
        "doc_type": category,
        "extracted_format": file_format,
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


@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    """
    파일 업로드 및 분석 엔드포인트
    
    Returns:
        표준화된 API 응답
    """
    try:
        logger.info("=" * 80)
        logger.info("📤 /api/upload 엔드포인트 호출됨")
        logger.info("=" * 80)
        
        # 1) 파일 꺼내기 (request.files 또는 data-url)
        if "file" in request.files:
            f = request.files["file"]
            if not f or f.filename == '':
                return create_error_response(
                    ErrorCode.FILE_NOT_FOUND,
                    details="파일이 선택되지 않았습니다"
                )
            
            filename = f.filename
            file_bytes = f.read()
            logger.info(f"📁 파일 업로드 (multipart): {filename}")
            
        else:
            data_url = request.form.get("file")
            if not data_url or not data_url.startswith("data:"):
                return create_error_response(
                    ErrorCode.FILE_NOT_FOUND,
                    details="파일 데이터가 없습니다"
                )

            try:
                header, b64 = data_url.split(",", 1)
                file_bytes = base64.b64decode(b64)
                mime = header.split(";")[0].split(":", 1)[1]
                ext = mimetypes.guess_extension(mime) or ""
                filename = f"upload{ext}"
                logger.info(f"📁 파일 업로드 (data URL): {filename}")
            except Exception as e:
                return create_error_response(
                    ErrorCode.FILE_VALIDATION_ERROR,
                    details=f"파일 디코딩 실패: {str(e)}"
                )

        logger.info(f"📏 파일 크기: {len(file_bytes):,} bytes")

        # 파일 크기 검증 (10MB)
        MAX_FILE_SIZE = 10 * 1024 * 1024
        if len(file_bytes) > MAX_FILE_SIZE:
            return create_error_response(
                ErrorCode.FILE_SIZE_ERROR,
                details=f"파일 크기: {len(file_bytes) / 1024 / 1024:.2f}MB (최대: 10MB)"
            )

        # 2) 포맷 판별
        fmt_enum = detect_file_format(file_bytes, filename)

        # 지원하지 않는 형식이면 에러
        if fmt_enum == FileFormat.UNKNOWN:
            logger.error(f"❌ 지원하지 않는 파일 형식: {filename}")
            return create_error_response(
                ErrorCode.FILE_FORMAT_ERROR,
                details=f"파일명: {filename}"
            )

        # Enum.value에서 실제 포맷 문자열 추출
        file_format = fmt_enum.value  # "pdf", "hwp", "word", "image"

        # form 옵션
        category = request.form.get("category", "etc")
        use_handwriting = request.form.get("use_handwriting", "false").lower() == "true"

        logger.info(f"📋 카테고리: {category}, 손글씨: {use_handwriting}, 포맷: {file_format}")

        # 3) 자동 분석 실행
        try:
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
        
        except Exception as e:
            logger.error(f"❌ LLM 분석 실패: {e}")
            return create_error_response(
                ErrorCode.LLM_FAILED,
                details=str(e),
                status_code=503
            )

        # 4) 응답 파싱 및 구조화
        try:
            structured_response = parse_llm_response(
                llm_response=raw_response,
                category=category,
                filename=filename,
                file_format=file_format
            )

            # 5) 디버그 로그
            logger.info("=" * 80)
            logger.info("📤 최종 응답 구조:")
            logger.info(f"  - file_name: {structured_response.get('file_name')}")
            logger.info(f"  - doc_type: {structured_response.get('doc_type')}")
            logger.info(f"  - extracted_format: {structured_response.get('extracted_format')}")
            if structured_response.get('summary'):
                logger.info(f"  - summary.title: {structured_response.get('summary', {}).get('title')}")
            logger.info("=" * 80)

            # 6) 표준화된 성공 응답 반환
            return create_success_response(structured_response)
            
        except Exception as e:
            logger.error(f"❌ 응답 파싱 실패: {e}")
            
            # 파싱 실패 시 폴백 응답 반환 (여전히 성공 응답으로)
            fallback_data = create_fallback_data(
                raw_response, category, filename, file_format
            )
            return create_success_response(fallback_data)

    except Exception as e:
        current_app.logger.exception("❌ /api/upload 오류")
        logger.error("=" * 80)
        logger.error(f"❌ /api/upload 오류: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        logger.error("=" * 80)
        
        return create_error_response(
            ErrorCode.INTERNAL_ERROR,
            details=str(e),
            status_code=500
        )
