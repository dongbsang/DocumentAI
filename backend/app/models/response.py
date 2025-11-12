"""
API 응답 표준 모델
"""
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ErrorCode(str, Enum):
    """에러 코드 정의"""
    # 파일 관련
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_FORMAT_ERROR = "FILE_FORMAT_ERROR"
    FILE_SIZE_ERROR = "FILE_SIZE_ERROR"
    FILE_VALIDATION_ERROR = "FILE_VALIDATION_ERROR"
    
    # OCR 관련
    OCR_FAILED = "OCR_FAILED"
    OCR_LOW_CONFIDENCE = "OCR_LOW_CONFIDENCE"
    
    # LLM 관련
    LLM_FAILED = "LLM_FAILED"
    LLM_TIMEOUT = "LLM_TIMEOUT"
    LLM_PARSE_ERROR = "LLM_PARSE_ERROR"
    
    # 서버 관련
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    
    # 요청 관련
    INVALID_REQUEST = "INVALID_REQUEST"
    MISSING_PARAMETER = "MISSING_PARAMETER"


class ErrorDetail:
    """에러 상세 정보"""
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        details: Optional[str] = None,
        suggestion: Optional[str] = None
    ):
        self.code = code.value
        self.message = message
        self.details = details
        self.suggestion = suggestion
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "code": self.code,
            "message": self.message
        }
        if self.details:
            result["details"] = self.details
        if self.suggestion:
            result["suggestion"] = self.suggestion
        return result


class ApiResponse:
    """API 응답 기본 클래스"""
    def __init__(
        self,
        success: bool,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[ErrorDetail] = None,
        request_id: Optional[str] = None
    ):
        self.success = success
        self.data = data
        self.error = error
        self.request_id = request_id
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.version = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error.to_dict() if self.error else None,
            "metadata": {
                "timestamp": self.timestamp,
                "version": self.version,
                "request_id": self.request_id
            }
        }


class SuccessResponse(ApiResponse):
    """성공 응답"""
    def __init__(
        self,
        data: Dict[str, Any],
        request_id: Optional[str] = None
    ):
        super().__init__(
            success=True,
            data=data,
            error=None,
            request_id=request_id
        )


class ErrorResponse(ApiResponse):
    """실패 응답"""
    def __init__(
        self,
        error: ErrorDetail,
        request_id: Optional[str] = None
    ):
        super().__init__(
            success=False,
            data=None,
            error=error,
            request_id=request_id
        )


# 에러 메시지 템플릿
ERROR_MESSAGES = {
    ErrorCode.FILE_NOT_FOUND: "파일을 찾을 수 없습니다",
    ErrorCode.FILE_FORMAT_ERROR: "지원하지 않는 파일 형식입니다",
    ErrorCode.FILE_SIZE_ERROR: "파일 크기가 제한을 초과했습니다",
    ErrorCode.FILE_VALIDATION_ERROR: "파일 검증에 실패했습니다",
    ErrorCode.OCR_FAILED: "OCR 처리에 실패했습니다",
    ErrorCode.OCR_LOW_CONFIDENCE: "OCR 신뢰도가 낮습니다",
    ErrorCode.LLM_FAILED: "LLM 분석에 실패했습니다",
    ErrorCode.LLM_TIMEOUT: "LLM 분석 시간이 초과되었습니다",
    ErrorCode.LLM_PARSE_ERROR: "LLM 응답 파싱에 실패했습니다",
    ErrorCode.INTERNAL_ERROR: "서버 내부 오류가 발생했습니다",
    ErrorCode.SERVICE_UNAVAILABLE: "서비스를 사용할 수 없습니다",
    ErrorCode.INVALID_REQUEST: "잘못된 요청입니다",
    ErrorCode.MISSING_PARAMETER: "필수 파라미터가 누락되었습니다",
}

# 에러별 제안 메시지
ERROR_SUGGESTIONS = {
    ErrorCode.FILE_FORMAT_ERROR: "PDF, 이미지(JPG, PNG), Word(.doc, .docx), HWP, TXT 파일을 업로드해주세요",
    ErrorCode.FILE_SIZE_ERROR: "파일 크기를 10MB 이하로 줄여주세요",
    ErrorCode.OCR_FAILED: "이미지 품질을 개선하거나 다른 파일을 시도해주세요",
    ErrorCode.LLM_FAILED: "잠시 후 다시 시도하거나 관리자에게 문의하세요",
}
