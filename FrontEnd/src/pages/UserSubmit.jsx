import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // <-- import useNavigate
import '../css/userSubmit.css';

export default function UserSubmit() {
  const [form, setForm] = useState({
    location: '',
    durationStart: '',
    durationEnd: '',
    companions: 1,
    concept: '',
    extra_request: '',
  });

  const navigate = useNavigate(); // <-- create navigator

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm(prev => ({
      ...prev,
      [name]: name === "companions" ? parseInt(value) || 0 : value,
    }));
  };


  const handleSubmit = () => {
    // Format data to match the shape expected by backend or next page
    const userData = {
      location: form.location,
      duration: {
        start: form.durationStart,
        end: form.durationEnd
      },
      companions: parseInt(form.companions, 10),
      concept: form.concept,
      extra_request: form.extra_request,
      kwargs: {
      filter:null,
      prev_map_data:null,
      poi_file_loc:null
    },
    };

    // Navigate to map_loading page with state
    navigate('/map_loading', { state: { userInput: userData } });
  };

  return (
    <div className="page-wrapper">
      <div className="form-container">
        <label htmlFor="location">Location:</label>
        <select name="location" id="location" value={form.location} onChange={handleChange}>
          <option value="">-- Select --</option>
          <option value="Seoul">Seoul</option>
          <option value="Busan">Busan</option>
        </select>

        <label htmlFor="durationStart">Duration Start:</label>
        <input
          type="date"
          id="durationStart"
          name="durationStart"
          value={form.durationStart}
          onChange={handleChange}
        />

        <label htmlFor="durationEnd">Duration End:</label>
        <input
          type="date"
          id="durationEnd"
          name="durationEnd"
          value={form.durationEnd}
          onChange={handleChange}
        />

        <label htmlFor="companions">Number of Companions:</label>
        <input
          type="number"
          id="companions"
          name="companions"
          min="1"
          max="10"
          value={form.companions}
          onChange={handleChange}
        />

        <label htmlFor="concept">Trip Concept:</label>
        <select name="concept" id="concept" value={form.concept} onChange={handleChange}>
          <option value="">-- Select --</option>
          <option value="Relaxing">Relaxing</option>
          <option value="Adventure">Adventure</option>
          <option value="Cultural">Cultural</option>
        </select>

        <label htmlFor="extra_request">Extra Request:</label>
        <input
          type="text"
          id="extra_request"
          name="extra_request"
          value={form.extra_request}
          onChange={handleChange}
        />

        <button onClick={handleSubmit}>Submit</button>
      </div>
    </div>
  );
}
