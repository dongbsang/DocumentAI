import axios from "axios";

// proxy 설정(package.json)을 사용하므로 상대 경로 사용
const API_BASE_URL = '/api';

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

    console.log('✅ 업로드 성공:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ 파일 업로드 실패:', error);
    
    if (error.response) {
      // 서버가 응답을 반환한 경우
      console.error('서버 응답 오류:', error.response.status, error.response.data);
      throw new Error(error.response.data?.error || `업로드 실패 (${error.response.status})`);
    } else if (error.request) {
      // 요청이 전송되었으나 응답을 받지 못한 경우
      console.error('서버 연결 오류:', error.request);
      throw new Error('서버와 연결할 수 없습니다. 백엔드가 실행 중인지 확인하세요.');
    } else {
      // 요청 설정 중 오류 발생
      console.error('요청 설정 오류:', error.message);
      throw new Error(error.message || '알 수 없는 오류가 발생했습니다.');
    }
  }
};

/**
 * 서버 상태 확인
 * @returns {Promise<Object>} 서버 상태
 */
export const checkServerStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/status`);
    return response.data;
  } catch (error) {
    console.error('서버 상태 확인 실패:', error);
    throw new Error('서버와 연결할 수 없습니다.');
  }
};
