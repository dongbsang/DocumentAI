import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import "../css/Result.css";

const Result = () => {
  const navigate = useNavigate();
  const { state } = useLocation();

  // 잘못된 접근 시 2초 뒤 홈으로 이동
  useEffect(() => {
    if (!state || !state.filename || !state.ocrResult) {
      const timer = setTimeout(() => {
        navigate("/", { replace: true });
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [state, navigate]);

  // state 검증
  if (!state || !state.filename || !state.ocrResult) {
    return (
      <div className="result-container">
        <p>잘못된 접근입니다. 홈으로 돌아갑니다.</p>
      </div>
    );
  }

  // ocrResult 에서 text, info 분리
  const { filename, ocrResult } = state;
  const { text, info } = ocrResult;

  const handleBackClick = () => {
    navigate("/");
  };

  const handleDownload = () => {
    // TODO: 파일명·내용을 묶어서 다운로드 로직 구현
    alert("결과 다운로드 기능은 아직 구현 중입니다.");
  };

  return (
    <div className="result-container">
      <h2 className="result-title">분석 결과</h2>

      <div className="result-box">
        <p>✅ 문서 분석이 완료되었습니다.</p>
        <p>📄 업로드된 파일명: <strong>{filename}</strong></p>

        <h3>OCR로 추출된 텍스트</h3>
        <pre className="ocr-text">{text}</pre>

        <h3>추출 정보</h3>
        <pre className="ocr-info">
          {JSON.stringify(info, null, 2)}
        </pre>
      </div>

      <div className="result-buttons">
        <button className="result-button" onClick={handleDownload}>
          결과 다운로드
        </button>
        <button className="result-button secondary" onClick={handleBackClick}>
          홈으로 돌아가기
        </button>
      </div>
    </div>
  );
};

export default Result;