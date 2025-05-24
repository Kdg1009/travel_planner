import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function SavedPlans() {
  const navigate = useNavigate();
  const [fileList, setFileList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/list_csv")
      .then((res) => res.json())
      .then(setFileList)
      .catch(() => setError("CSV 목록을 불러오지 못했습니다."));
  }, []);

  const parseCsv = (text) => {
    const lines = text.trim().split("\n");
    const headers = lines[0].split(",");
    return lines.slice(1).map((line) => {
      const values = line.split(",");
      return headers.reduce((obj, header, idx) => {
        obj[header.trim()] = values[idx].trim();
        return obj;
      }, {});
    });
  };

  const toScheduleObject = (parsedArray) => {
    const schedule = {};
    parsedArray.forEach((entry) => {
      const day = entry["DAY"];
      const place = entry["PLACE"];
      if (!schedule[day]) schedule[day] = [];
      schedule[day].push(place);
    });
    return schedule;
  };

  const handleClick = async (filename) => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/load_csv?file=${filename}`);
      const text = await res.text();
      const parsed = parseCsv(text);
      const schedule = toScheduleObject(parsed);
      navigate("/result", { state: { schedule } });
    } catch (e) {
      setError("파일을 불러오는 데 실패했습니다.");
    }
    setLoading(false);
  };

  return (
    <div className="p-8 max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">📁 저장된 일정 선택</h1>

      {error && <p className="text-red-500">{error}</p>}
      {loading && <p>⏳ 불러오는 중...</p>}

      <ul className="space-y-2">
        {fileList.map((file) => (
          <li
            key={file}
            className="cursor-pointer px-4 py-2 bg-gray-100 rounded hover:bg-blue-100"
            onClick={() => handleClick(file)}
          >
            {file}
          </li>
        ))}
      </ul>

      <button
        onClick={() => navigate("/main")}
        className="px-4 py-2 bg-gray-300 rounded mt-6"
      >
        메인화면으로 돌아가기
      </button>
    </div>
  );
}