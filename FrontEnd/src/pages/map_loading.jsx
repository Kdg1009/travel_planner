import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

export default function MapLoading() {
  const location = useLocation();
  const userInput = location.state?.userInput;
  const [mapData, setMapData] = useState(null);

  useEffect(() => {
    const fetchMapData = async () => {
      try {
        const res = await fetch("http://localhost:8000/get_pois", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(userInput),
        });
        const data = await res.json();
        setMapData(data);
      } catch (err) {
        console.error("Failed to fetch POIs:", err);
      }
    };

    fetchMapData();
  }, [userInput]);

  if (!mapData) {
    return <div>🗺️ Loading your map recommendation...</div>;
  }

  return (
    <div>
      <h2>🎉 Map Ready!</h2>
      <pre>{JSON.stringify(mapData, null, 2)}</pre>
    </div>
  );
}
