import React from "react";
import { useNavigate } from "react-router-dom";

export default function MainPage() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-6">
      <h1 className="text-3xl font-bold mb-4">🗺️ Welcome to 저기어때!</h1>

      <button
        className="bg-blue-500 text-white px-6 py-2 rounded shadow"
        onClick={() => navigate("/input")}
      >
        여행 정보 입력
      </button>

      <button
        className="bg-green-500 text-white px-6 py-2 rounded shadow"
        onClick={() => navigate("/theme")}
      >
        테마 선택
      </button>

      <button
        className="bg-purple-500 text-white px-6 py-2 rounded shadow"
        onClick={() => navigate("/saved")}
      >
        저장된 일정 보기
      </button>

      <button
        className="bg-yellow-500 text-white px-6 py-2 rounded shadow"
        onClick={() => navigate("/map")}
      >
        지도에서 보기
      </button>

      <button
        className="bg-red-500 text-white px-6 py-2 rounded shadow"
        onClick={() => navigate("/result")}
      >
        결과 보기
      </button>
    </div>
  );
}