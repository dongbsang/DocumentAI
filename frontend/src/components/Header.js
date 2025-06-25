import React from 'react'
import '../css/Header.css'

const Header = () => {

    const handleMenuClick =() => {
        alert("어떤 기능을 넣을까")
    }


  return (
    <header className="home-header">
        <h1 className="home-title">AI 도큐먼트 파트너</h1>
        <button className="menu-button" onClick={handleMenuClick}>☰</button>
    </header>
  );
}

export default Header