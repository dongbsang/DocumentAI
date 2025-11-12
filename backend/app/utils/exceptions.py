"""
커스텀 예외 클래스
"""
from app.models.response import ErrorCode


class DocumentAIException(Exception):
    """기본 예외 클래스"""
    def __init__(self, message: str, error_code: ErrorCode, details: str = None):
        self.message = message
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)


class FileProcessingError(DocumentAIException):
    """파일 처리 관련 에러"""
    def __init__(self, message: str, details: str = None, file_name: str = None):
        self.file_name = file_name
        super().__init__(
            message=message,
            error_code=ErrorCode.FILE_VALIDATION_ERROR,
            details=details
        )


class OCRError(DocumentAIException):
    """OCR 처리 에러"""
    def __init__(self, message: str, details: str = None, confidence: float = None):
        self.confidence = confidence
        super().__init__(
            message=message,
            error_code=ErrorCode.OCR_FAILED,
            details=details
        )


class LLMError(DocumentAIException):
    """LLM 관련 에러"""
    def __init__(self, message: str, details: str = None, model: str = None):
        self.model = model
        super().__init__(
            message=message,
            error_code=ErrorCode.LLM_FAILED,
            details=details
        )


class LLMTimeoutError(DocumentAIException):
    """LLM 타임아웃 에러"""
    def __init__(self, message: str, timeout: int = None):
        self.timeout = timeout
        super().__init__(
            message=message,
            error_code=ErrorCode.LLM_TIMEOUT,
            details=f"LLM 응답 시간 초과 ({timeout}초)" if timeout else None
        )


class ParseError(DocumentAIException):
    """파싱 에러"""
    def __init__(self, message: str, details: str = None, raw_data: str = None):
        self.raw_data = raw_data[:500] if raw_data else None  # 처음 500자만 저장
        super().__init__(
            message=message,
            error_code=ErrorCode.LLM_PARSE_ERROR,
            details=details
        )


class ServiceUnavailableError(DocumentAIException):
    """서비스 사용 불가 에러"""
    def __init__(self, message: str, service_name: str = None):
        self.service_name = service_name
        super().__init__(
            message=message,
            error_code=ErrorCode.SERVICE_UNAVAILABLE,
            details=f"서비스: {service_name}" if service_name else None
        )
