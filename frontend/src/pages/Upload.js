import React, { useState } from 'react';
import '../css/Upload.css';
import { useNavigate } from 'react-router-dom';
import ProgressBar from '../components/ProgressBar';

const apiUrl = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

const Upload = () => {
  const [fileName, setFileName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [category, setCategory] = useState('이력서');
  const [useHandwriting, setUseHandwriting] = useState(false);
  const [loading, setLoading] = useState(false);
  const [progressStep, setProgressStep] = useState(0);

  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) {
      alert('파일을 선택해주세요.');
      return;
    }
    setFileName(file.name);
    setSelectedFile(file);
  };

  const handleResultClick = async () => {
    if (!selectedFile) return alert('파일을 선택해주세요.');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('category', category);
    formData.append('use_handwriting', useHandwriting);

    try {
      setLoading(true);
      setProgressStep(1); // 1단계: 분석 시작
      setProgressStep(2); // 2단계: 분석 중

      const response = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
        body: formData,
        // FormData를 쓸 때는 Content-Type 자동 설정되므로 헤더 넣지 말 것!
      });

      // 응답 바디를 먼저 파싱
      let result;
      try {
        result = await response.json();
      } catch {
        // JSON 파싱 자체가 실패하는 경우
        throw new Error(`서버 응답 파싱 실패 (${response.status})`);
      }

      // 상태코드 에러 or 서버가 { error: "..."} 반환한 경우
      if (!response.ok || result?.error) {
        const msg = result?.error || `업로드 실패 (${response.status})`;
        throw new Error(msg);
      }

      setProgressStep(3); // 3단계: 완료!

      // 문자열 렌더링 보장 (React에서 객체를 바로 렌더링하면 에러)
      const safeSummary =
        typeof result.summary === 'string'
          ? result.summary
          : JSON.stringify(result.summary ?? '', null, 2);

      const safeInfo =
        typeof result.info === 'string'
          ? result.info
          : JSON.stringify(result.info ?? '', null, 2);

      // 세션 저장
      const payload = {
        filename: result.filename ?? fileName ?? '',
        summary: safeSummary,
        info: safeInfo,
      };
      sessionStorage.setItem('analysisResult', JSON.stringify(payload));

      // 페이지 이동
      navigate('/result', { state: payload });
    } catch (err) {
      console.error('분석 중 오류:', err);
      alert(err?.message || '분석 중 오류가 발생했습니다.');
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
          <option value="이력서">이력서</option>
          <option value="영수증">영수증</option>
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
          accept="image/*,application/pdf"
          onChange={handleFileChange}
          className="file-input"
        />
        <span>파일을 클릭하거나 드래그해서 업로드하세요</span>
      </label>

      {fileName && <div className="file-name">📄 {fileName}</div>}

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