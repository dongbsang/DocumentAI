import React, { useState } from 'react';
import '../css/Upload.css';
import { useNavigate } from 'react-router-dom';
import ProgressBar from '../components/ProgressBar';
import { uploadFile } from '../api';

const Upload = () => {
  const [fileName, setFileName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [category, setCategory] = useState('resume');
  const [useHandwriting, setUseHandwriting] = useState(false);
  const [loading, setLoading] = useState(false);
  const [progressStep, setProgressStep] = useState(0);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) {
      alert('파일을 선택해주세요.');
      return;
    }

    // 파일 크기 검증 (10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      alert(`파일 크기가 너무 큽니다 (최대 10MB)\n현재: ${(file.size / 1024 / 1024).toFixed(2)}MB`);
      return;
    }

    setFileName(file.name);
    setSelectedFile(file);
    setError(null);
  };

  const handleResultClick = async () => {
    if (!selectedFile) {
      alert('파일을 선택해주세요.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setProgressStep(1); // 1단계: 분석 시작
      setProgressStep(2); // 2단계: 분석 중

      // api.js의 uploadFile 함수 사용 (표준화된 응답 받음)
      const result = await uploadFile(selectedFile, category, useHandwriting);

      console.log('📦 백엔드 응답:', result);

      setProgressStep(3); // 3단계: 완료!

      // ✅ 표준화된 응답 구조에서 데이터 추출
      // result = {
      //   file_name: "...",
      //   doc_type: "...",
      //   extracted_format: "...",
      //   summary: {...},
      //   details: {...},
      //   meta: {...}
      // }

      // ✅ 기존 Result.js 및 View 컴포넌트와 호환되는 구조로 전달
      const payload = {
        filename: result.file_name,
        data: {
          summary: result.summary,    // ✅ 기존 구조 유지
          details: result.details,    // ✅ 기존 구조 유지
          meta: result.meta           // ✅ 기존 구조 유지
        },
        category: result.doc_type,
        extractedFormat: result.extracted_format,
      };

      console.log('📤 Result 페이지로 전달할 데이터:', payload);

      // 세션 저장
      sessionStorage.setItem('analysisResult', JSON.stringify(payload));

      // 페이지 이동
      navigate('/result', { state: payload });
      
    } catch (err) {
      console.error('❌ 분석 중 오류:', err);
      
      setProgressStep(0);

      // 에러 메시지 구성
      let errorMessage = err.message || '분석 중 오류가 발생했습니다';

      if (err.details) {
        errorMessage += `\n\n상세: ${err.details}`;
      }

      if (err.suggestion) {
        errorMessage += `\n\n💡 ${err.suggestion}`;
      }

      setError(errorMessage);
      alert(errorMessage);
      
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <button className="back-button" onClick={() => navigate(-1)}>← 뒤로가기</button>
      <h2 className="upload-title">문서 업로드</h2>

      <div className="category-section">
        <label>문서 카테고리:</label>
        <select value={category} onChange={e => setCategory(e.target.value)}>
          <option value="resume">이력서</option>
          <option value="receipt">영수증</option>
          <option value="diagnosis">진단서</option>
          <option value="etc">기타</option>
        </select>
      </div>

      <div className="handwriting-checkbox">
        <label>
          <input
            type="checkbox"
            checked={useHandwriting}
            onChange={e => setUseHandwriting(e.target.checked)}
          />
          손글씨 포함
        </label>
      </div>

      <label className="upload-box">
        <input
          type="file"
          accept="image/*,application/pdf,.doc,.docx,.hwp,.txt"
          onChange={handleFileChange}
          className="file-input"
        />
        <span>파일을 클릭하거나 드래그해서 업로드하세요</span>
        <span className="file-size-hint" style={{ fontSize: '0.85em', color: '#666', marginTop: '5px' }}>
          최대 10MB
        </span>
      </label>

      {fileName && (
        <div className="file-name">
          📄 {fileName}
          {selectedFile && (
            <span style={{ fontSize: '0.9em', color: '#666', marginLeft: '10px' }}>
              ({(selectedFile.size / 1024 / 1024).toFixed(2)}MB)
            </span>
          )}
        </div>
      )}

      {error && (
        <div className="error-message" style={{ 
          padding: '15px', 
          backgroundColor: '#fee', 
          border: '1px solid #fcc',
          borderRadius: '5px',
          marginTop: '15px',
          whiteSpace: 'pre-line'
        }}>
          <p style={{ margin: 0, color: '#c33' }}>{error}</p>
        </div>
      )}

      <button
        className="analyze-button"
        disabled={!selectedFile || loading}
        onClick={handleResultClick}
      >
        {loading ? '분석 중...' : '분석 시작'}
      </button>

      {loading && <ProgressBar step={progressStep} />}
      {loading && <div className="overlay" />}
    </div>
  );
};

export default Upload;
