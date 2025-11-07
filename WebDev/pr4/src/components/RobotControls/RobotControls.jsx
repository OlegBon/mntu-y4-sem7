import React from "react";

// Отримуємо функції з props
function RobotControls({
  onStartMission,
  onReturnToBase,
  isStartMissionDisabled,
  isReturnToBaseDisabled,
}) {
  return (
    <div>
      <h4>Керування</h4>
      <button onClick={onStartMission} disabled={isStartMissionDisabled}>
        Відправити
      </button>

      <button
        onClick={onReturnToBase}
        style={{ marginLeft: "10px" }}
        disabled={isReturnToBaseDisabled}
      >
        На базу
      </button>
    </div>
  );
}

export default RobotControls;
