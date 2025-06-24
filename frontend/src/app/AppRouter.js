import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Home from "../pages/Home";

const AppRouter = () => {
  //const isAuth = true; // 실제 인증 여부로 교체하세요

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="*" element={<div>404 - 페이지를 찾을 수 없습니다.</div>} />
    </Routes>
  );
};

export default AppRouter;