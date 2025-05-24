import React, { useEffect, useRef } from "react";

export default function MapVisualize({ route }) {
  const mapRef = useRef(null);

  useEffect(() => {
    if (!window.naver || !mapRef.current || !Array.isArray(route)) return;

    const map = new window.naver.maps.Map(mapRef.current, {
      center: new window.naver.maps.LatLng(route[0]?.lat || 33.4, route[0]?.long || 126.3),
      zoom: 10,
    });

    const pathCoords = [];

    route.forEach((poi) => {
      if (!poi?.lat || !poi?.long) return;
      const pos = new window.naver.maps.LatLng(poi.lat, poi.long);
      pathCoords.push(pos);

      new window.naver.maps.Marker({
        map,
        position: pos,
        title: poi.name,
      });
    });

    new window.naver.maps.Polyline({
      map,
      path: pathCoords,
      strokeColor: "#FF0000",
      strokeWeight: 3,
    });
  }, [route]);

  return <div id="map" ref={mapRef} style={{ width: "100%", height: "500px" }} />;
}