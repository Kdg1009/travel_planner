import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  GeoJSON,
} from "react-leaflet";
import L from "leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";

// Marker defaults
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

export default function MapVisualize() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const travelPlan = state.travelPlan;
  const userRequest = state.userRequest;

  const [selectedDayIndex, setSelectedDayIndex] = useState(0);
  const [routeGeoJson, setRouteGeoJson] = useState(null);
  const [email, setEmail] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loadingRoute, setLoadingRoute] = useState(false);
  const [currentPlaces, setCurrentPlaces] = useState([]);

  const isInvalidPlan = !travelPlan?.plans || travelPlan.plans.length === 0;

  const getLatLng = (loc) => {
    if (!loc || loc.latitude == null || loc.longitude == null) {
      console.warn("Invalid location object:", loc);
      return [37.5665, 126.9780]; // Seoul default
    }
    return [loc.latitude, loc.longitude];
  };

  const getORSCoords = (list) =>
    list.map((v) => [v.location.longitude, v.location.latitude]);

  useEffect(() => {
    if (isInvalidPlan) return;

    const day = travelPlan.plans[selectedDayIndex];
    const places = day?.place_to_visit || [];

    setCurrentPlaces(places);
    setRouteGeoJson(null); // Clear route before fetching

    if (places.length < 2) return;

    setLoadingRoute(true);
    axios
      .post("http://localhost:8000/api/ors_proxy", {
        coordinates: getORSCoords(places),
      })
      .then((res) => setRouteGeoJson(res.data))
      .catch((err) => {
        console.error("Route fetch failed", err);
        setRouteGeoJson(null);
      })
      .finally(() => setLoadingRoute(false));
  }, [selectedDayIndex, travelPlan, isInvalidPlan]);

  const handleSendEmail = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/save_plan",
        {
          user_id: userRequest.kwargs.cache_key,
          travel_plan: travelPlan,
        },
        {
          responseType: "blob",
        }
      );

      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "travel_plan.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();

      alert("plan downloaded!");
    } catch (err) {
      console.error("Email send failed", err);
    }
  };

  const handleRetry = async () => {
    const updatedUserRequest = {
      ...userRequest,
      extra_request: feedback,
    };
    navigate("/map_loading", { state: { userInput: updatedUserRequest } });
  };

  return (
    <div>
      {isInvalidPlan ? (
        <>
          <h2>Error</h2>
          <p>No day plans found in the travel plan.</p>
          <button onClick={() => navigate(-1)}>Go Back</button>
        </>
      ) : (
        <>
          <h2>Final Route</h2>

          <select
            onChange={(e) => setSelectedDayIndex(Number(e.target.value))}
            value={selectedDayIndex}
          >
            {travelPlan.plans.map((day, i) => (
              <option key={i} value={i}>
                Day {i + 1}: {day.date}
              </option>
            ))}
          </select>

          {loadingRoute && <p>Loading route...</p>}

          {currentPlaces.length > 0 && (
            <MapContainer
              center={getLatLng(currentPlaces[0].location)}
              zoom={13}
              style={{ height: "500px", width: "100%", marginTop: "1em" }}
              key={selectedDayIndex}
            >
              <TileLayer
                attribution='&copy; <a href="https://osm.org">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              {currentPlaces.map((visit, i) => (
                <Marker key={i} position={getLatLng(visit.location)}>
                  <Popup>
                    <strong>{visit.name}</strong> <br />
                    Concept: {visit.concept.join(", ")} <br />
                    Address: {visit.address || "N/A"} <br />
                  </Popup>
                </Marker>
              ))}
              {routeGeoJson && <GeoJSON data={routeGeoJson} />}
            </MapContainer>
          )}

          <div style={{ marginTop: "1em" }}>
            <h3>Send to Email</h3>
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <button disabled={!email} onClick={handleSendEmail}>
              Send
            </button>
          </div>

          <div style={{ marginTop: "1em" }}>
            <h3>Retry with Feedback</h3>
            <textarea
              placeholder="Add feedback to improve the plan"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
            />
            <button disabled={!feedback} onClick={handleRetry}>
              Retry
            </button>
          </div>
        </>
      )}
    </div>
  );
}
