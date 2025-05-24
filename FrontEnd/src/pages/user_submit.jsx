import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { UserData } from "../components/user_data"; // 통합 user_data 경로

export default function InputForm() {
  const navigate = useNavigate();
  const location = useLocation();
  const selectedTheme = location.state?.selectedTheme || "";

  const [form, setForm] = useState({
    name: "",
    region: "",
    date: "",
    theme: selectedTheme,
    people: 1,
    budget: 0,
    location: "",
    durationStart: "",
    durationEnd: "",
    companions: "",
    concept: "",
    extra_request: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
  e.preventDefault();

  const userData = new UserData();
  userData.name = form.name;
  userData.region = form.region;
  userData.date = form.date;
  userData.theme = form.theme;
  userData.people = form.people;
  userData.budget = form.budget;
  userData.location = form.location;
  userData.duration = {
    start: form.durationStart,
    end: form.durationEnd,
  };
  userData.companions = form.companions;
  userData.concept = form.concept;
  userData.extra_request = form.extra_request;

  navigate("/result", { state: { userInput: userData.toJSON() } });
};

  return (
    <form onSubmit={handleSubmit} style={{ padding: "2rem" }}>
      <h2>여행 정보 입력</h2>

      <label>이름: <input type="text" name="name" value={form.name} onChange={handleChange} /></label><br />
      <label>지역: <input type="text" name="region" value={form.region} onChange={handleChange} /></label><br />
      <label>날짜: <input type="date" name="date" value={form.date} onChange={handleChange} /></label><br />
      <label>인원수: <input type="number" name="people" value={form.people} onChange={handleChange} /></label><br />
      <label>예산: <input type="number" name="budget" value={form.budget} onChange={handleChange} /></label><br />
      <label>테마: <input type="text" name="theme" value={form.theme} onChange={handleChange} /></label><br />
      <label>여행 위치: <input type="text" name="location" value={form.location} onChange={handleChange} /></label><br />
      <label>시작일: <input type="date" name="durationStart" value={form.durationStart} onChange={handleChange} /></label><br />
      <label>종료일: <input type="date" name="durationEnd" value={form.durationEnd} onChange={handleChange} /></label><br />
      <label>동행자: <input type="text" name="companions" value={form.companions} onChange={handleChange} /></label><br />
      <label>여행 컨셉: <input type="text" name="concept" value={form.concept} onChange={handleChange} /></label><br />
      <label>추가 요청사항: <textarea name="extra_request" value={form.extra_request} onChange={handleChange} /></label><br />

      <button type="submit">다음</button>
    </form>
  );
}

