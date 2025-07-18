import React from 'react';
import '../css/ProgressBar.css';

const stepMessages = {
  1: '① 문서 유형 확인 중...',
  5: '② 문서 분석 중...',
  6: '③ 분석 완료!',
};

/**
 * ProgressBar 컴포넌트
 * @param {Object} props
 * @param {number} props.step - 현재 진행 단계
 * @returns {JSX.Element}
 */
const ProgressBar = ({ step }) => {
  const message = stepMessages[step] || '잠시만 기다려주세요...';

  return (
    <div className="progress-container">
      <div className="spinner" />
      <div className="progress-message">{message}</div>
    </div>
  );
};

export default ProgressBar;