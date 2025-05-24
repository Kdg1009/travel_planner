import { useLocation } from "react-router-dom";

export default function MapVisualize() {
  const { state } = useLocation();
  return (
    <div>
      <h2>Final Route</h2>
      <ul>
        {state.route.map((poi, i) => (
          <li key={i}>{poi.name} ({poi.lat}, {poi.long})</li>
        ))}
      </ul>
    </div>
  );
}