// src/components/ScheduleViewer.jsx
import React from 'react';
import styles from './ScheduleViewer.module.css';

export default function ScheduleViewer({ places, segments = [] }) {
    if (!places || places.length === 0) {
        return <p className="text-gray-500">📭 일정이 비어있습니다.</p>;
    }

    return (
        <ul className={styles.list}>
            {places.map((place, index) => (
                <React.Fragment key={index}>
                <li className={styles.item}>
                    <div className={styles.name}>📍 {place.name}</div>
                    <div className={styles.detail}>
                        위도: {place.location.latitude}, 경도: {place.location.longitude}
                    </div>
                    <div className={styles.concepts}>
                        🧭 {place.concept?.join(', ') || 'N/A'}
                    </div>
                </li>

                {/* 마지막 장소가 아니라면 이동 정보 추가 */}
                {segments && index < segments.length && (
                    <li className={styles.transition}>
                        ↓ 약 {(segments[index].distance / 1000).toFixed(1)}km / {Math.round(segments[index].duration / 60)}분
                    </li>
                )}
            </React.Fragment>
            ))}
        </ul>
    );
}