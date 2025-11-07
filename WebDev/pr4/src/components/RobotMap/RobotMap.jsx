import React from "react";
import "./RobotMap.css";

// Отримує позицію робота зі стану
function RobotMap({ position, basePosition }) {
  if (!position || !basePosition) {
    return <div className="map-container">...Завантаження карти...</div>;
  }

  // inline-стилі, щоб динамічно задавати позицію іконки робота
  const robotStyle = {
    top: `${position.y}px`,
    left: `${position.x}px`,
  };
  const bazaStyle = {
    top: `${basePosition.y}px`,
    left: `${basePosition.x}px`,
  };

  return (
    <div className="map-container">
      <div className="map-background">
        <div className="baza-icon" style={bazaStyle}>
          База
          <img src="/img/baza.png" alt="Baza" />
        </div>
        <div className="robot-icon" style={robotStyle}>
          <img src="/img/robot.png" alt="Robot" />
        </div>
      </div>
    </div>
  );
}

export default RobotMap;
