import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import MapVisualize from "./MapVisualize";

export default function MapPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const userInput = location.state?.userData || {};
  const travelPlan = location.state?.travelPlan || {};

  const [feedback, setFeedback] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!location.state?.userData || !location.state?.travelPlan) {
      alert("잘못된 접근입니다. 메인 페이지로 돌아갑니다.");
      navigate("/");
    }
  }, [location.state, navigate]);

  const handleSave = async () => {
    try {
      const res = await fetch("http://localhost:3000/api/save_pois", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ poi_list: userInput?.locationData || [], filename: "saved_route.csv" }),
      });
      const result = await res.text();
      alert("저장이 완료되었습니다.\n" + result);
    } catch (err) {
      console.error("저장 실패:", err);
      alert("저장 중 오류 발생");
    }
  };

  const handleFeedback = async () => {
    setIsLoading(true);
    try {
      const updatedUser = {
        ...userInput,
        extra_request: feedback,
      };

      const res = await fetch("http://localhost:3000/api/route_optim", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedUser),
      });

      const data = await res.json();
      navigate("/map", {
        state: {
          userData: data.user_data,
          travelPlan: data.travel_plan,
        },
      });
    } catch (err) {
      console.error("피드백 전송 실패:", err);
      alert("요청 중 오류 발생");
    }
    setIsLoading(false);
  };

  return (
    <div className="flex h-screen">
      {/* 일정표 영역 */}
      <div className="w-2/3 overflow-y-auto border-r p-6">
        <h2 className="text-xl font-bold mb-4">📅 일정표</h2>
        {Object.entries(travelPlan).map(([day, places]) => (
          <div key={day} className="mb-6">
            <h3 className="font-semibold text-lg mb-2">{day}</h3>
            <ul className="space-y-2">
              {places.map((place) => (
                <li key={place} className="border p-2 rounded">
                  {place}
                </li>
              ))}
            </ul>
          </div>
        ))}

        <div className="mt-6">
          <textarea
            className="w-full h-24 border p-2 rounded"
            placeholder="추가 요청사항을 입력하세요"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />
          <div className="mt-2 flex gap-4">
            <button
              onClick={handleSave}
              className="bg-blue-600 text-white px-4 py-2 rounded"
            >
              저장하기
            </button>
            <button
              onClick={handleFeedback}
              className="bg-green-600 text-white px-4 py-2 rounded"
              disabled={isLoading}
            >
              {isLoading ? "전송 중..." : "피드백 전송"}
            </button>
          </div>
        </div>
      </div>

      {/* 지도 영역 */}
      <div className="w-1/3 p-6">
        <MapVisualize
          route={
            Object.values(travelPlan).flat().map((name, i) => ({
              name,
              lat: userInput?.locationData?.[name]?.lat || 33.4 + i * 0.01,
              long: userInput?.locationData?.[name]?.long || 126.3 + i * 0.01,
            }))
          }
        />
      </div>
    </div>
  );
}
