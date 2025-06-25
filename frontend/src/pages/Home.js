import React from 'react'
import '../App.css'
import '../css/Home.css'
import { useNavigate } from 'react-router-dom'

const Home = () => {
  const navigate = useNavigate();

  const handleStartClick =() => {
    navigate('/upload');
  }

  return (
   <div className="home-container">
      {/* 본문 */}
      <main className="home-main">
        <h2 className="main-title">AI 분석 시작하기</h2>
        <p className="main-description">
          업무를 자동화하고 싶은가요?<br />
          다양한 문서를 AI로 분석하세요.
        </p>
        <button className="start-button"onClick={handleStartClick}>분석 시작</button>
      </main>
    </div>
  )
}

export default Home
