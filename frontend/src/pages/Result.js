import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import "../css/Result.css";

const Result = () => {
      const navigate = useNavigate();
  const { state } = useLocation();

  // 만약 직접 URL 진입 등으로 state가 없으면 홈으로 리다이렉트
  if (!state || !state.filename || !state.ocrResult) {
    return (
      <div className="result-container">
        <p>잘못된 접근입니다. 홈으로 돌아갑니다.</p>
        {setTimeout(() => navigate("/"), 2000)}
      </div>
    );
  }

  const { filename, ocrResult } = state; 
  // ocrResult: { text: "...", info: { 키: 값, ... } }

  //처음으로 돌아가기
  const handleBackClick = () => {
    navigate("/");
  };

  //결과 다운로드 (추후 구현)
  const handleDownload = () => {
    alert("결과 다운로드 중... (실제 구현 필요)");
  };
    
  return (
    <div className="result-container">
      <h2 className="result-title">분석 결과</h2>

      <div className="result-box">
        <p>✅ 문서 분석이 완료되었습니다.</p>

        {/* 1) 업로드된 파일명 */}
        <p>📄 업로드된 파일명: <strong>{filename}</strong></p>

        {/* 2) OCR 텍스트 */}
        <h3>OCR로 추출된 텍스트</h3>
        <pre className="ocr-text">{ocrResult}</pre>

        {/* 3) GPT Vision 등 추가 정보 */}
        <h3>추출 정보</h3>
        <pre className="ocr-info">
          {JSON.stringify(ocrResult.info, null, 2)}
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
}

export default Result;