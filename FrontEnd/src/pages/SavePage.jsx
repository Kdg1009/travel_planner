import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./SavePage.module.css";

export default function SavePage() {
  const navigate = useNavigate();
  const [files, setFiles] = useState([]);
  const [selected, setSelected] = useState("");

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/list_csv");
        const data = await res.json();
        setFiles(data);
      } catch (err) {
        console.error("Failed to load saved files", err);
      }
    };
    fetchFiles();
  }, []);

  const handleDownload = () => {
    if (!selected) return;
    const link = document.createElement("a");
    link.href = `http://localhost:8000/api/download_csv?filename=${selected}`;
    link.setAttribute("download", selected);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>저기어때 – AI 여행 가이드</div>
      <h2 className={styles.title}>〈저장된 일정 확인하기〉</h2>

      <div className={styles.fileList}>
        {files.length > 0 ? (
          files.map((filename, idx) => (
            <button
              key={idx}
              className={`${styles.fileButton} ${selected === filename ? styles.selected : ""}`}
              onClick={() => setSelected(filename)}
            >
              {idx + 1}. {filename.replace(".csv", "")}
            </button>
          ))
        ) : (
          <p className={styles.empty}>저장된 일정이 없습니다.</p>
        )}
      </div>

      <div className={styles.buttonRow}>
        <button onClick={() => navigate("/")} className={styles.navButton}>
          메인메뉴로 돌아가기
        </button>
        <button
          onClick={handleDownload}
          disabled={!selected}
          className={styles.downloadButton}
        >
          일정 다운로드하기
        </button>
      </div>
    </div>
  );
}