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

    try {
      setLoading(true);
      setProgressStep(1); // 1단계: 분석 시작
      setProgressStep(2); // 2단계: 분석 중

      // api.js의 uploadFile 함수 사용
      const result = await uploadFile(selectedFile, category, useHandwriting);

      console.log('📦 백엔드 응답:', result);

      setProgressStep(3); // 3단계: 완료!

      // ✅ 백엔드 응답 구조에 맞게 데이터 추출
      // result = {
      //   success: true,
      //   file_name: "...",
      //   data: {
      //     summary: {...},
      //     details: {...},
      //     meta: {...}
      //   }
      // }

      if (!result.success) {
        throw new Error('분석에 실패했습니다.');
      }

      // OCR 텍스트는 summary의 description 또는 전체 summary를 표시
      const ocrText = result.data?.summary?.description || 
                      JSON.stringify(result.data?.summary || {}, null, 2);

      // 추출 정보는 details + meta를 합쳐서 표시
      const extractedInfo = {
        ...result.data?.details,
        ...result.data?.meta
      };

      // 세션 저장
      const payload = {
        filename: result.file_name || fileName,
        data: result.data,  // 전체 데이터 구조 전달
        category: category,  // 카테고리 정보 전달
      };

      console.log('📤 Result 페이지로 전달할 데이터:', payload);

      sessionStorage.setItem('analysisResult', JSON.stringify(payload));

      // 페이지 이동
      navigate('/result', { state: payload });
    } catch (err) {
      console.error('❌ 분석 중 오류:', err);
      alert(err?.message || '분석 중 오류가 발생했습니다.');
      setProgressStep(0);
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
          accept="image/*,application/pdf,.doc,.docx"
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
