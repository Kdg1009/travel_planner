import React from 'react';
import { Routes, Route } from 'react-router-dom';
import UserSubmit from './pages/UserSubmit';
import MapLoading from './pages/MapLoading';
import MapVisualize from './pages/MapVisualize';

function App() {
  return (
    <Routes>
      <Route path="/" element={<UserSubmit />} />
      <Route path="/map_loading" element={<MapLoading />} />
      <Route path="/map_visualize" element={<MapVisualize />} />
    </Routes>
  );
}

export default App;