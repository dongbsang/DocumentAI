import React, { useState } from 'react';
import '../css/Upload.css';
import { useNavigate } from 'react-router-dom';

const Upload = () => {
  const [fileName, setFileName] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name);
    }
    };

  //되돌리기 
  const handleBack =() => {
      navigate(-1);
    }
  
  //결과페이지
  const handleResultClick =() => {
      navigate('/result');
    }
  

  return (
    <div className="upload-container">
    <button className="back-button" onClick={handleBack}>
        ← 뒤로가기
    </button>
      <h2 className="upload-title">문서 업로드</h2>

      <label className="upload-box">
        <input type="file" onChange={handleFileChange} className="file-input" />
        <span>파일을 여기에 드래그하거나 클릭해서 업로드하세요</span>
      </label>

      {fileName && <div className="file-name">📄 {fileName}</div>}

      <button className="analyze-button" disabled={!fileName} onClick={handleResultClick}>
        분석 시작
      </button>
    </div>
  );
};

export default Upload;