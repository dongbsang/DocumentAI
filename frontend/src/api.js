import axios from 'axios';
import { validateApiResponse, getErrorMessage, getErrorDetails } from './types/api';

const API_BASE_URL = '/api';

/**
 * API 에러 클래스
 */
class ApiError extends Error {
  constructor(message, code, details, suggestion) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.details = details;
    this.suggestion = suggestion;
  }
}

/**
 * 파일 업로드 및 분석
 * @param {File} file - 업로드할 파일
 * @param {string} category - 문서 카테고리 (이력서, 영수증, etc)
 * @param {boolean} useHandwriting - 손글씨 인식 여부
 * @returns {Promise<Object>} 분석 결과
 */
export const uploadFile = async (file, category = 'resume', useHandwriting = false) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('category', category);
  formData.append('use_handwriting', useHandwriting);

  try {
    console.log('📤 업로드 시작:', {
      fileName: file.name,
      fileSize: `${(file.size / 1024 / 1024).toFixed(2)}MB`,
      category,
      useHandwriting,
      url: `${API_BASE_URL}/upload`
    });

    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 120000, // 120초 타임아웃 (LLM 처리 시간 고려)
    });

    const data = response.data;

    console.log('📦 백엔드 원본 응답:', data);

    // 응답 구조 검증
    try {
      validateApiResponse(data);
    } catch (validationError) {
      console.error('❌ 응답 검증 실패:', validationError);
      throw new ApiError(
        '서버 응답 형식이 올바르지 않습니다',
        'INVALID_RESPONSE',
        validationError.message,
        null
      );
    }

    // 성공 응답
    if (data.success) {
      console.log('✅ 업로드 성공:', {
        fileName: data.data.file_name,
        docType: data.data.doc_type,
        requestId: data.metadata?.request_id,
        timestamp: data.metadata?.timestamp
      });
      return data.data;
    }

    // 실패 응답
    const errorMessage = getErrorMessage(data);
    const errorDetails = getErrorDetails(data);

    console.error('❌ 업로드 실패:', {
      code: data.error.code,
      message: errorMessage,
      details: errorDetails,
    });

    throw new ApiError(
      errorMessage,
      data.error.code,
      data.error.details,
      data.error.suggestion
    );

  } catch (error) {
    // Axios 에러 처리
    if (error instanceof ApiError) {
      throw error;
    }

    if (error.response) {
      // 서버 응답 있음
      const data = error.response.data;

      if (data && data.error) {
        const errorMessage = getErrorMessage(data);
        throw new ApiError(
          errorMessage,
          data.error.code,
          data.error.details,
          data.error.suggestion
        );
      }

      throw new ApiError(
        `서버 오류 (${error.response.status})`,
        'HTTP_ERROR',
        error.response.statusText,
        null
      );
    }

    if (error.request) {
      // 요청 전송됐으나 응답 없음
      console.error('❌ 서버 연결 오류:', error.request);
      throw new ApiError(
        '서버와 연결할 수 없습니다',
        'NETWORK_ERROR',
        '백엔드 서버가 실행 중인지 확인하세요',
        'Flask 서버를 시작해주세요: flask run'
      );
    }

    // 기타 오류
    console.error('❌ 알 수 없는 오류:', error);
    throw new ApiError(
      error.message || '알 수 없는 오류가 발생했습니다',
      'UNKNOWN_ERROR',
      null,
      null
    );
  }
};

/**
 * 서버 상태 확인
 * @returns {Promise<Object>} 서버 상태
 */
export const checkServerStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/status`, {
      timeout: 5000,
    });
    return response.data;
  } catch (error) {
    console.error('서버 상태 확인 실패:', error);
    throw new ApiError(
      '서버와 연결할 수 없습니다',
      'SERVER_UNAVAILABLE',
      null,
      null
    );
  }
};
