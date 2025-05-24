import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import MainPage from './pages/MainPage';
import InputPage from './pages/user_submit';      // 원래 파일명 기준
import ThemePage from './pages/ThemePage';
import SavedPlans from './pages/SavedPlans';
import MapPage from './pages/MapPage';
import ResultPage from './pages/ResultPage';

export default function App() {
  return (
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/input" element={<InputPage />} />
        <Route path="/theme" element={<ThemePage />} />
        <Route path="/saved" element={<SavedPlans />} />
        <Route path="/map" element={<MapPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
  );
}