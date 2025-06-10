import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./SavePage.module.css";
import { useUser } from "../context/UserContext";

export default function SavePage() {
  const navigate = useNavigate();
  const { user } = useUser();
  const UserId = user?.id || "";
  const [plans, setPlans] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(null);

  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/load_plans?user_id=${UserId}`);
        const data = await res.json(); // data.value is list of DB_TravelPlan
        setPlans(data.value || []);
      } catch (err) {
        console.error("Failed to load plans", err);
      }
    };
    fetchPlans();
  }, []);

  const handleShowPlan = () => {
    if (selectedIndex === null) return;
    const selectedPlan = plans[selectedIndex];
    navigate("/map_visualize", {
      state: { travelPlan: selectedPlan.travel_plan },
    });
  };

  const handleDelete = async (plan, idx) => {
    const confirm = window.confirm(`Delete "${plan.title}"?`);
    if (!confirm) return;

    try {
      const res = await fetch(`/api/delete_plan?_id=${plan._id}`, {
        method: "DELETE",
      });
      const data = await res.json();
      if (data.success) {
        const newPlans = plans.filter((_, i) => i !== idx);
        setPlans(newPlans);
        setSelectedIndex(null);
      } else {
        const data = await res.json();
        alert(`Error: ${data.detail}`);
      }
    } catch (err) {
      console.error(err);
      alert("Error deleting plan.");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>저기어때 – AI 여행 가이드</div>
      <h2 className={styles.title}>〈저장된 일정 확인하기〉</h2>

      <div className={styles.fileList} style={{ maxHeight: "300px", overflowY: "auto" }}>
        {plans.length > 0 ? (
          plans.map((plan, idx) => (
            <div key={plan._id || idx} style={{ display: "flex", alignItems: "center", marginBottom: "4px" }}>
              <button
                className={`${styles.fileButton} ${selectedIndex === idx ? styles.selected : ""}`}
                onClick={() => setSelectedIndex(idx)}
              >
                {idx + 1}. {plan.title}
            </button>
              {selectedIndex === idx && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(plan, idx);
                  }}
                  className={styles.deleteButton}
                >
                  Delete
                </button>
              )}
            </div>
          ))
        ) : (
          <p>No plans available.</p>
        )}
      </div>

      <div className={styles.buttonRow}>
        <button onClick={() => navigate("/")} className={styles.navButton}>
          메인메뉴로 돌아가기
        </button>
        <button
          onClick={handleShowPlan}
          disabled={selectedIndex === null}
          className={styles.showplanButton}
        >
          일정 보여주기
        </button>
      </div>
    </div>
  );
}