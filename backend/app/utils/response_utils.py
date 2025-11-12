"""
API 응답 유틸리티 함수
"""
import uuid
from typing import Dict, Any, Optional
from flask import jsonify

from app.models.response import (
    SuccessResponse,
    ErrorResponse,
    ErrorDetail,
    ErrorCode,
    ERROR_MESSAGES,
    ERROR_SUGGESTIONS
)


def create_success_response(
    data: Dict[str, Any],
    status_code: int = 200
) -> tuple:
    """
    성공 응답 생성

    Args:
        data: 응답 데이터
        status_code: HTTP 상태 코드

    Returns:
        tuple: (jsonify response, status_code)
    """
    request_id = str(uuid.uuid4())[:8]
    response = SuccessResponse(data=data, request_id=request_id)
    return jsonify(response.to_dict()), status_code


def create_error_response(
    error_code: ErrorCode,
    details: Optional[str] = None,
    custom_message: Optional[str] = None,
    status_code: int = 400
) -> tuple:
    """
    에러 응답 생성

    Args:
        error_code: 에러 코드 (ErrorCode enum)
        details: 에러 상세 정보
        custom_message: 커스텀 에러 메시지 (없으면 기본 메시지 사용)
        status_code: HTTP 상태 코드

    Returns:
        tuple: (jsonify response, status_code)
    """
    request_id = str(uuid.uuid4())[:8]

    message = custom_message or ERROR_MESSAGES.get(
        error_code,
        "알 수 없는 오류가 발생했습니다"
    )

    suggestion = ERROR_SUGGESTIONS.get(error_code)

    error = ErrorDetail(
        code=error_code,
        message=message,
        details=details,
        suggestion=suggestion
    )

    response = ErrorResponse(error=error, request_id=request_id)
    return jsonify(response.to_dict()), status_code
