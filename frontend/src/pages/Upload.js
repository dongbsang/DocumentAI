import React, { useState } from 'react';
import '../css/Upload.css';
import { useNavigate } from 'react-router-dom';

const apiUrl = process.env.REACT_APP_API_BASE_URL;

const Upload = () => {
  const [fileName, setFileName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [category, setCategory] = useState('자기소개서');
  const [useHandwriting, setUseHandwriting] = useState(false);

  const navigate = useNavigate();

  // 파일 업로드
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name);
      setSelectedFile(file);
    }
  };

  // 되돌리기
  const handleBack = () => {
    navigate(-1);
  };

  // 결과 페이지로 이동 + 분석 요청
  const handleResultClick = async () => {
    if (!selectedFile) return alert('파일을 선택해주세요.');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('category', category);
    formData.append('use_handwriting', useHandwriting);

    console.log('API URL:', apiUrl);  // 디버깅용 출력

    try {
      const response = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      navigate('/result', {
        state: {
                filename: result.filename,
                ocrResult: result.ocr_result
              }
      });
    } catch (error) {
      console.error('OCR 요청 실패:', error);
      alert('분석 중 오류 발생');
    }
  };

  return (
    <div className="upload-container">
      <button className="back-button" onClick={handleBack}>← 뒤로가기</button>
      <h2 className="upload-title">문서 업로드</h2>

      {/* 카테고리 선택 */}
      <div className="category-section">
        <label>문서 카테고리:</label>
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="자기소개서">자기소개서</option>
          <option value="영수증">영수증</option>
          <option value="etc">기타</option>
        </select>
      </div>

      {/* 손글씨 체크 */}
      <div className="handwriting-checkbox">
        <label>
          <input
            type="checkbox"
            checked={useHandwriting}
            onChange={(e) => setUseHandwriting(e.target.checked)}
          />
          손글씨 포함
        </label>
      </div>

      {/* 파일 업로드 */}
      <label className="upload-box">
        <input type="file" onChange={handleFileChange} className="file-input" />
        <span>파일을 여기에 드래그하거나 클릭해서 업로드하세요</span>
      </label>

      {/* 파일 이름 표시 */}
      {fileName && <div className="file-name">📄 {fileName}</div>}

      {/* 분석 버튼 */}
      <button className="analyze-button" disabled={!fileName} onClick={handleResultClick}>
        분석 시작
      </button>
    </div>
  );
};

export default Upload;