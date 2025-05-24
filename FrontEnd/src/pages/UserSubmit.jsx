import styles from '../css/userSubmit.css';
import "../css/userSubmit.css"
import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { UserData } from "../components/user_data"; // adjust path if needed

export default function UserSubmit() {
  const [form, setForm] = useState({
    location: "",
    durationStart: "",
    durationEnd: "",
    companions: 1,
    concept: "",
    extra_request: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    const intValue = parseInt(value, 10);

    setForm((prevForm) => ({
      ...prevForm,
      [name]: name === "companions"
        ? (isNaN(intValue) ? "" : Math.min(intValue, 10))
        : value,
    }));
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
  // <start> this is for when error occurs at mapLoading page and returned from it
  const location = useLocation();
  const savedInput = location.state?.userInput;

  useEffect(() => {
    if (savedInput) {
      setForm({
        location: savedInput.location || "",
        durationStart: savedInput.duration?.start || "",
        durationEnd: savedInput.duration?.end || "",
        companions: savedInput.companions || 0,
        concept: savedInput.concept || "",
        extra_request: savedInput.extra_request || "",
      });
    }
  }, [savedInput]);
  // <end> error handling part
  return (
    <div className='page-wrapper'>
      <div className="form-container">
        <div className={styles.container}>
          <h2>Plan Your Trip</h2>

          <label className={styles.label}>Location:</label>
          <select
            name="location"
            value={form.location}
            onChange={handleChange}
            className={styles.select}
          >
            <option value="">-- Select --</option>
            <option value="Seoul">Seoul</option>
            <option value="Busan">Busan</option>
          </select>

          <label className={styles.label}>Duration Start:</label>
          <input
            type="date"
            name="durationStart"
            value={form.durationStart}
            onChange={handleChange}
            className={styles.input}
          />

          <label className={styles.label}>Duration End:</label>
          <input
            type="date"
            name="durationEnd"
            value={form.durationEnd}
            onChange={handleChange}
            className={styles.input}
          />

          <label className={styles.label}>Number of Companions:</label>
          <input
            type="number"
            name="companions"
            value={form.companions}
            onChange={handleChange}
            min="1"
            max="10"
            className={styles.input}
          />

          <label className={styles.label}>Trip Concept:</label>
          <select
            name="concept"
            value={form.concept}
            onChange={handleChange}
            className={styles.select}
          >
            <option value="">-- Select --</option>
            <option value="Relaxing">Relaxing</option>
            <option value="Adventure">Adventure</option>
            <option value="Cultural">Cultural</option>
          </select>

          <label className={styles.label}>Extra Request:</label>
          <input
            type="text"
            name="extra_request"
            value={form.extra_request}
            onChange={handleChange}
            className={styles.input}
          />

          <button onClick={handleSubmit} className={styles.button}>
            Submit
          </button>
        </div>
      </div>
    </div>
  );
}
