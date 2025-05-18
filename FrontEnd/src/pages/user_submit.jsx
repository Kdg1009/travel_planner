import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { UserData } from "../user_data"; // adjust path if needed

export default function UserSubmit() {
  const [form, setForm] = useState({
    location: "",
    durationStart: "",
    durationEnd: "",
    companions: "",
    concept: "",
    extra_request: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = () => {
    const userData = new UserData();
    userData.location = form.location;
    userData.duration = { start: form.durationStart, end: form.durationEnd };
    userData.companions = form.companions;
    userData.concept = form.concept;
    userData.extra_request = form.extra_request;

    navigate("/map_loading", { state: { userInput: userData.toJSON() } });
  };

  return (
    <div>
      <h2>Plan Your Trip</h2>

      <label>Location:</label>
      <select name="location" value={form.location} onChange={handleChange}>
        <option value="">-- Select --</option>
        <option value="Seoul">Seoul</option>
        <option value="Busan">Busan</option>
      </select>

      <label>Duration Start:</label>
      <input type="date" name="durationStart" value={form.durationStart} onChange={handleChange} />

      <label>Duration End:</label>
      <input type="date" name="durationEnd" value={form.durationEnd} onChange={handleChange} />

      <label>Companions:</label>
      <select name="companions" value={form.companions} onChange={handleChange}>
        <option value="">-- Select --</option>
        <option value="Solo">Solo</option>
        <option value="Couple">Couple</option>
        <option value="Family">Family</option>
      </select>

      <label>Trip Concept:</label>
      <select name="concept" value={form.concept} onChange={handleChange}>
        <option value="">-- Select --</option>
        <option value="Relaxing">Relaxing</option>
        <option value="Adventure">Adventure</option>
        <option value="Cultural">Cultural</option>
      </select>

      <label>Extra Request:</label>
      <input type="text" name="extra_request" value={form.extra_request} onChange={handleChange} />

      <br />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}
