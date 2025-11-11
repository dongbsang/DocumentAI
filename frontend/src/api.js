import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

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
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // 60초 타임아웃
    });

    return response.data;
  } catch (error) {
    console.error('파일 업로드 실패:', error);
    
    if (error.response) {
      // 서버가 응답을 반환한 경우
      throw new Error(error.response.data?.error || `업로드 실패 (${error.response.status})`);
    } else if (error.request) {
      // 요청이 전송되었으나 응답을 받지 못한 경우
      throw new Error('서버와 연결할 수 없습니다. 백엔드가 실행 중인지 확인하세요.');
    } else {
      // 요청 설정 중 오류 발생
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
