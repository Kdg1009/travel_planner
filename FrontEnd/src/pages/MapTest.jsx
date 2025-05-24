import React, { useEffect, useRef } from "react";

export default function MapPage() {
    useEffect(() => {
  fetch("/testroute.json") // ✅ 슬래시 올바름 + 위치 맞음
    .then(res => res.json())
    .then(data => {
      console.log(data); // 테스트 확인용
    });
}, []);
  // 예시 일정
  const schedule = {
    "DAY 1": ["성산일출봉", "오설록 티뮤지엄"]
  };

  // POI 좌표 데이터
  const route = [
    { name: "성산일출봉", lat: 33.4589, long: 126.9411 },
    { name: "오설록 티뮤지엄", lat: 33.3059, long: 126.2883 }
  ];

  const mapRef = useRef(null);

  useEffect(() => {
    if (!window.naver || !mapRef.current) return;

    const map = new window.naver.maps.Map(mapRef.current, {
      center: new window.naver.maps.LatLng(route[0].lat, route[0].long),
      zoom: 10,
    });

    const pathCoords = [];

    route.forEach((poi) => {
      const pos = new window.naver.maps.LatLng(poi.lat, poi.long);
      pathCoords.push(pos);

      new window.naver.maps.Marker({
        map: map,
        position: pos,
        title: poi.name,
      });
    });

    new window.naver.maps.Polyline({
      map: map,
      path: pathCoords,
      strokeColor: "#FF0000",
      strokeWeight: 3,
    });
  }, []);

  return (
    <div className="flex h-screen">
      {/* 왼쪽: 일정표 */}
      <div className="w-2/3 overflow-y-auto border-r p-6">
        <h2 className="text-xl font-bold mb-4">📅 일정표</h2>
        {Object.entries(schedule).map(([day, places]) => (
          <div key={day} className="mb-6">
            <h3 className="font-semibold text-lg mb-2">{day}</h3>
            <ul className="space-y-2">
              {places.map((place, i) => (
                <li key={i} className="border p-2 rounded">{place}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* 오른쪽: 지도 */}
      <div className="w-1/3 p-6">
        <div id="map" ref={mapRef} style={{ width: "100%", height: "500px" }} />
      </div>
    </div>
  );
}