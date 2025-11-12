import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import ReceiptView from '../components/ReceiptView';
import ResumeView from '../components/ResumeView';
import GenericView from '../components/GenericView';
import "../css/Result.css";

const Result = () => {
  const navigate = useNavigate();
  const { state } = useLocation();

  // 잘못된 접근 시 2초 뒤 홈으로 이동
  useEffect(() => {
    if (!state || !state.data) {
      const timer = setTimeout(() => {
        navigate("/", { replace: true });
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [state, navigate]);

  // state 검증
  if (!state || !state.data) {
    return (
      <div className="result-container">
        <div className="error-message">
          <p>잘못된 접근입니다. 홈으로 돌아갑니다.</p>
        </div>
      </div>
    );
  }

  const { filename, data, category } = state;

  const handleBackClick = () => {
    navigate("/");
  };

  const handleDownload = () => {
    // JSON 데이터를 파일로 다운로드
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename.split('.')[0]}_분석결과.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // 카테고리별 컴포넌트 렌더링
  const renderCategoryView = () => {
    console.log('📊 카테고리:', category);
    console.log('📦 데이터:', data);

    switch (category) {
      case 'receipt':
        return <ReceiptView data={data} />;
      case 'resume':
        return <ResumeView data={data} />;
      case 'diagnosis':
      case 'etc':
      default:
        return <GenericView data={data} category={category} />;
    }
  };

  return (
    <div className="result-container">
      <div className="result-header">
        <h2 className="result-title">✅ 문서 분석 완료</h2>
        <p className="result-filename">
          📄 <strong>{filename}</strong>
        </p>
      </div>

      {/* 카테고리별 렌더링 */}
      {renderCategoryView()}

      {/* 하단 버튼 */}
      <div className="result-buttons">
        <button className="result-button primary" onClick={handleDownload}>
          📥 결과 다운로드 (JSON)
        </button>
        <button
          className="result-button secondary"
          onClick={handleBackClick}
        >
          🏠 홈으로 돌아가기
        </button>
      </div>
    </div>
  );
};

export default Result;
