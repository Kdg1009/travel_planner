import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ThemePage() {
  const navigate = useNavigate();
  const [selectedTheme, setSelectedTheme] = useState("");

  const handleThemeSelect = (theme) => {
    setSelectedTheme(theme);
  };

  const handleNext = () => {
    navigate("/", { state: { selectedTheme } }); // user_submit로 이동
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">테마를 선택하세요</h2>
      <div className="flex gap-4 mb-4">
        <button onClick={() => handleThemeSelect("힐링")}>힐링</button>
        <button onClick={() => handleThemeSelect("액티비티")}>액티비티</button>
        <button onClick={() => handleThemeSelect("문화")}>문화</button>
      </div>
      <button
        onClick={handleNext}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        다음
      </button>
    </div>
  );
}
