/**
 * API 응답 타입 정의
 */

// 에러 코드
export const ErrorCode = {
  FILE_NOT_FOUND: 'FILE_NOT_FOUND',
  FILE_FORMAT_ERROR: 'FILE_FORMAT_ERROR',
  FILE_SIZE_ERROR: 'FILE_SIZE_ERROR',
  FILE_VALIDATION_ERROR: 'FILE_VALIDATION_ERROR',
  OCR_FAILED: 'OCR_FAILED',
  OCR_LOW_CONFIDENCE: 'OCR_LOW_CONFIDENCE',
  LLM_FAILED: 'LLM_FAILED',
  LLM_TIMEOUT: 'LLM_TIMEOUT',
  LLM_PARSE_ERROR: 'LLM_PARSE_ERROR',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  SERVICE_UNAVAILABLE: 'SERVICE_UNAVAILABLE',
  INVALID_REQUEST: 'INVALID_REQUEST',
  MISSING_PARAMETER: 'MISSING_PARAMETER',
};

// 사용자 친화적 에러 메시지
export const ERROR_MESSAGES = {
  [ErrorCode.FILE_NOT_FOUND]: '파일을 찾을 수 없습니다',
  [ErrorCode.FILE_FORMAT_ERROR]: '지원하지 않는 파일 형식입니다',
  [ErrorCode.FILE_SIZE_ERROR]: '파일 크기가 너무 큽니다 (최대 10MB)',
  [ErrorCode.FILE_VALIDATION_ERROR]: '파일 검증에 실패했습니다',
  [ErrorCode.OCR_FAILED]: 'OCR 처리에 실패했습니다',
  [ErrorCode.OCR_LOW_CONFIDENCE]: 'OCR 신뢰도가 낮습니다',
  [ErrorCode.LLM_FAILED]: '문서 분석에 실패했습니다',
  [ErrorCode.LLM_TIMEOUT]: '분석 시간이 초과되었습니다',
  [ErrorCode.LLM_PARSE_ERROR]: '분석 결과 처리에 실패했습니다',
  [ErrorCode.INTERNAL_ERROR]: '서버 오류가 발생했습니다',
  [ErrorCode.SERVICE_UNAVAILABLE]: '서비스를 사용할 수 없습니다',
  [ErrorCode.INVALID_REQUEST]: '잘못된 요청입니다',
  [ErrorCode.MISSING_PARAMETER]: '필수 정보가 누락되었습니다',
};

/**
 * API 응답 구조 검증
 */
export const validateApiResponse = (response) => {
  if (!response || typeof response !== 'object') {
    throw new Error('응답이 올바르지 않습니다');
  }

  if (typeof response.success !== 'boolean') {
    throw new Error('응답 형식이 올바르지 않습니다');
  }

  if (response.success) {
    if (!response.data) {
      throw new Error('응답 데이터가 없습니다');
    }
  } else {
    if (!response.error) {
      throw new Error('에러 정보가 없습니다');
    }
  }

  return true;
};

/**
 * 에러 메시지 추출
 */
export const getErrorMessage = (response) => {
  if (!response || !response.error) {
    return '알 수 없는 오류가 발생했습니다';
  }

  const error = response.error;

  // 커스텀 메시지가 있으면 사용
  if (error.message) {
    return error.message;
  }

  // 에러 코드에 해당하는 메시지 반환
  if (error.code && ERROR_MESSAGES[error.code]) {
    return ERROR_MESSAGES[error.code];
  }

  return '알 수 없는 오류가 발생했습니다';
};

/**
 * 에러 상세 정보 추출
 */
export const getErrorDetails = (response) => {
  if (!response || !response.error) {
    return null;
  }

  const details = [];

  if (response.error.details) {
    details.push(response.error.details);
  }

  if (response.error.suggestion) {
    details.push(`💡 ${response.error.suggestion}`);
  }

  return details.length > 0 ? details.join('\n') : null;
};
