import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

export default function MapLoading() {
  const location = useLocation();
  const navigate = useNavigate();
  const userInput = location.state?.userInput;

  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("Starting map generation...");

  useEffect(() => {
    const fetchMapData = async () => {
      try {
        setProgress(10);
        setStatus("Fetching POIs...");

        const getPoisRes = await fetch("http://localhost:3000/api/get_pois", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(userInput),
        });

        const poisData = await getPoisRes.json();
        const userData = poisData.user_data;

        setProgress(50);
        setStatus("Optimizing route...");

        const routeOptimRes = await fetch("http://localhost:3000/api/route_optim", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(userData),
        });

        const routeData = await routeOptimRes.json();
        const travelPlan = routeData.travel_plan;

        setProgress(100);
        setStatus("Map ready! Redirecting...");

        setTimeout(() => {
          navigate("/map/result", {
            state: {
              userData: routeData.user_data,
              travelPlan: travelPlan,
            },
          });
        }, 1000);
      } catch (err) {
        console.error("Failed to fetch data:", err);
        alert("⚠️ Internal server error occurred. Please try again later.");
        navigate("/", { state: { userInput: userInput } });
      }
    };

    fetchMapData();
  }, [userInput, navigate]);

  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h2>🗺️ Generating Your Travel Map</h2>
      <p>{status}</p>

      <div style={{ background: '#eee', height: '20px', width: '100%', maxWidth: '500px', margin: '1rem auto', borderRadius: '10px' }}>
        <div
          style={{
            background: '#4caf50',
            height: '100%',
            width: `${progress}%`,
            transition: 'width 0.5s ease-in-out',
            borderRadius: '10px'
          }}
        />
      </div>
    </div>
  );
}
