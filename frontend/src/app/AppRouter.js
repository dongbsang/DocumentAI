import React from "react";
import {Routes, Route} from "react-router-dom";
import Home from "../pages/Home";
import Header from "../components/Header";
import Upload from "../pages/Upload";
import Result from "../pages/Result";

const AppRouter = () => {
  return (
    <>
    <Header/>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/result" element={<Result />} />
        <Route path="*" element={<div>404 - 페이지를 찾을 수 없습니다.</div>} />
      </Routes>
    </>
  );
};

export default AppRouter;