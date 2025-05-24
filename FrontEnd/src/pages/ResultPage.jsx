import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const userInput = location.state?.userInput || {};

  const initialSchedule = {
    "DAY 1": ["협재 해수욕장", "곽지해수욕장"],
    "DAY 2": ["성산일출봉", "오설록 티뮤지엄"],
  };

  const [schedule, setSchedule] = useState(initialSchedule);
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [requestText, setRequestText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const placeInfo = {
    "협재 해수욕장": "제주의 대표 해수욕장, 맑은 바다와 하얀 모래가 특징",
    "곽지해수욕장": "현지인들도 즐겨 찾는 한적한 해변",
    "성산일출봉": "제주의 동쪽 해돋이 명소, 유네스코 세계자연유산",
    "오설록 티뮤지엄": "녹차 밭과 박물관이 있는 관광 명소",
  };

  const handleViewMap = () => {
    navigate("/map", { state: { userInput } });
  };

  const handleScheduleUpdate = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/route_optim", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userInput, request: requestText }),
      });
      const data = await res.json();
      if (data.schedule) setSchedule(data.schedule); // 예: {"DAY 1": [...], "DAY 2": [...]}
    } catch (err) {
      console.error("일정 수정 실패:", err);
    }
    setIsLoading(false);
  };

  return (
    <div className="flex h-screen">
      {/* 일정표 + 수정 */}
      <div className="w-2/3 overflow-y-auto border-r p-6">
        <h2 className="text-xl font-bold mb-4">📅 일정표</h2>
        {Object.entries(schedule).map(([day, places]) => (
          <div key={day} className="mb-6">
            <h3 className="font-semibold text-lg mb-2">{day}</h3>
            <ul className="space-y-2">
              {places.map((place) => (
                <li
                  key={place}
                  className={`border p-2 rounded cursor-pointer ${
                    selectedPlace === place ? "bg-blue-100" : ""
                  }`}
                  onClick={() => setSelectedPlace(place)}
                >
                  {place}
                </li>
              ))}
            </ul>
          </div>
        ))}

        <div className="mt-6">
          <h2 className="text-lg font-bold mb-2">✏️ 일정 수정 요청</h2>
          <textarea
            className="w-full h-32 border p-2 rounded"
            placeholder="예: 1일차에 박물관을 더 추가해줘"
            value={requestText}
            onChange={(e) => setRequestText(e.target.value)}
          />
          <button
            onClick={handleScheduleUpdate}
            className="mt-2 bg-green-600 text-white px-4 py-2 rounded"
            disabled={isLoading}
          >
            {isLoading ? "요청 중..." : "LLM에 일정 수정 요청하기"}
          </button>
        </div>

        <button
          onClick={handleViewMap}
          className="mt-6 bg-blue-600 text-white px-4 py-2 rounded"
        >
          지도에서 보기
        </button>
      </div>

      {/* 장소 상세정보 */}
      <div className="w-1/3 p-6">
        {selectedPlace ? (
          <>
            <h2 className="text-xl font-bold mb-2">{selectedPlace}</h2>
            <p className="mb-4">{placeInfo[selectedPlace]}</p>
          </>
        ) : (
          <p>장소를 선택하면 상세 정보가 나타납니다.</p>
        )}
      </div>
    </div>
  );
}