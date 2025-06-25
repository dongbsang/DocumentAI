import React from 'react'
import { useNavigate } from 'react-router-dom'
import "../css/Result.css"

const Result = () => {
    const navigate = useNavigate();

    const handleBackClick = () =>{
        navigate("/");
    }

    const handleDownload = () => {
        alert("결과 다운로드 중... (실제 구현 필요)");
    };



  return (
  <div className="result-container">
      <h2 className="result-title">분석 결과</h2>

      <div className="result-box">
        <p>✅ 문서 분석이 완료되었습니다.</p>
        <p>📄 총 3개의 항목이 추출되었습니다.</p>
        <p>💡 예: 계약자명, 계약일자, 총 금액</p>
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
  )
}

export default Result