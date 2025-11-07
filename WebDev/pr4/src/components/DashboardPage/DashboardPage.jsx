import "./DashboardPage.css";
import React from "react";
import RobotControls from "../RobotControls/RobotControls";
import RobotMap from "../RobotMap/RobotMap";

function DashboardPage({
  robotsData,
  selectedRobotId,
  isLoading,
  isBusy,
  handleCommand,
  handleSelectRobot,
}) {
  const LOW_BATTERY_THRESHOLD = 30; // Порог низького заряду батареї

  const activeRobot = robotsData.find((r) => r.id === selectedRobotId);

  if (isLoading || !activeRobot) {
    return (
      <div>
        <h2>Моніторинг</h2>
        <p>Завантаження даних про роботів...</p>
      </div>
    );
  }

  const isOnBase = activeRobot.status === "Charging"; // Робот на базі
  const hasEnoughBattery = activeRobot.battery >= LOW_BATTERY_THRESHOLD; // Достатній заряд батареї

  // Стан кнопок в залежності від статусу робота
  let isStartMissionDisabled = false;
  let isReturnToBaseDisabled = false;

  if (isBusy) {
    isStartMissionDisabled = true;
    isReturnToBaseDisabled = true;
  } else if (isOnBase) {
    isStartMissionDisabled = false;
    isReturnToBaseDisabled = true;
  } else if (!hasEnoughBattery) {
    isStartMissionDisabled = true;
    isReturnToBaseDisabled = false;
  } else {
    isStartMissionDisabled = false;
    isReturnToBaseDisabled = false;
  }

  return (
    <div>
      <h2>Моніторинг</h2>
      <div className="robot-selector">
        Оберіть робота:
        <select value={selectedRobotId} onChange={handleSelectRobot}>
          {robotsData.map((robot) => (
            <option key={robot.id} value={robot.id}>
              {robot.name}
            </option>
          ))}
        </select>
      </div>
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <RobotMap
            position={activeRobot.position}
            basePosition={activeRobot.basePosition}
          />
        </div>

        <div className="status-panel">
          {(() => {
            const isStranded =
              activeRobot.battery === 0 && activeRobot.status !== "Charging";
            const displayStatus = isStranded ? "Stranded" : activeRobot.status;
            return (
              <h3 style={{ color: isStranded ? "red" : "inherit" }}>
                Статус: {displayStatus}
              </h3>
            );
          })()}
          <p>ID Робота: {activeRobot.id}</p>
          <p>Заряд батареї: {activeRobot.battery}%</p>
          <p>
            Позиція: X: {activeRobot.position.x}, Y: {activeRobot.position.y}
          </p>

          <hr />

          <RobotControls
            onStartMission={() => handleCommand("start-mission")}
            onReturnToBase={() => handleCommand("return-to-base")}
            isStartMissionDisabled={isStartMissionDisabled}
            isReturnToBaseDisabled={isReturnToBaseDisabled}
          />
        </div>
      </div>{" "}
    </div>
  );
}

export default DashboardPage;
