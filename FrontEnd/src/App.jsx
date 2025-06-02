import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/Login';
import RegisterPage from './pages/UserRegister';
import MapLoading from './pages/MapLoading';
import MapVisualize from './pages/MapVisualize';
import UserSubmit from './pages/UserSubmit';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/user_submit" element={<UserSubmit />} />
      <Route path="/map_loading" element={<MapLoading />} />
      <Route path="/map_visualize" element={<MapVisualize />} />
    </Routes>
  );
};

export default App;
