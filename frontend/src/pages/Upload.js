import React, { useState } from 'react';
import '../css/Upload.css';
import { useNavigate } from 'react-router-dom';
import ProgressBar from '../components/ProgressBar';

const apiUrl = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000/api";


const Upload = () => {
  const [fileName, setFileName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [category, setCategory] = useState('이력서');
  const [useHandwriting, setUseHandwriting] = useState(false);
  const [loading, setLoading] = useState(false);
  const [progressStep, setProgressStep] = useState(0);

  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
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
      });


      if (!response.ok) throw new Error(response.statusText);

      const result = await response.json();
      setProgressStep(3); // 3단계: 완료!

      sessionStorage.setItem('analysisResult', JSON.stringify({
        filename: result.filename,
        summary: result.summary,
        info: result.info,
      }));

      navigate('/result', {
        state: {
          filename: result.filename,
          summary: result.summary,
          info: result.info,
        },
      });
    } catch (err) {
      console.error('분석 중 오류:', err);
      alert('분석 중 오류가 발생했습니다.');
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
        <select
          value={category}
          onChange={e => setCategory(e.target.value)}
        >
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
      {loading && <div className="overlay" />} {/* ✅ 전체 잠금 오버레이 */}
    </div>
  );
};

export default Upload;
