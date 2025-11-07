import "./App.css";
import { Routes, Route } from "react-router-dom";
import { useState, useEffect } from "react";
import DashboardPage from "./components/DashboardPage/DashboardPage";
import LogPage from "./components/LogPage/LogPage";
import Navbar from "./components/Navbar/Navbar";
import { fetchRobotsData, sendRobotCommand } from "./api/robot-api";

function App() {
  const [logs, setLogs] = useState([]); // Масив логів
  const [robotsData, setRobotsData] = useState([]); // Дані про роботів
  const [selectedRobotId, setSelectedRobotId] = useState(null); // Вибраний робот
  const [isLoading, setIsLoading] = useState(true); // Стан завантаження
  const [isBusy, setIsBusy] = useState(false); // Стан зайнятості робота

  // Функція для додавання логу
  const addLog = (robotName, message) => {
    const timestamp = new Date().toLocaleTimeString();
    const newLog = `${timestamp} - [${robotName}]: ${message}`;
    setLogs((prevLogs) => [newLog, ...prevLogs]);
  };

  // Завантаження даних про роботів при монтуванні компонента
  useEffect(() => {
    const loadData = async () => {
      const data = await fetchRobotsData();
      setRobotsData(data);
      setSelectedRobotId(data[0].id);
      setIsLoading(false);
      addLog("System", "Дані роботів успішно завантажено.");
    };
    loadData();
  }, []); // Порожній масив = виконати 1 раз

  // Обробка команд для робота
  const handleCommand = async (command) => {
    if (!selectedRobotId || isBusy) return;
    setIsBusy(true);

    const robot = robotsData.find((r) => r.id === selectedRobotId);
    const robotName = robot ? robot.name : "Unknown Robot";
    addLog(robotName, `Отримав команду '${command}'.`);

    const { newRobotsState } = await sendRobotCommand(
      command,
      robotsData,
      selectedRobotId
    );

    // Додавання логу про оновлення стану робота
    const updatedRobot = newRobotsState.find((r) => r.id === selectedRobotId);
    addLog(
      robotName,
      `Стан оновлено: ${updatedRobot.status}, Батарея: ${updatedRobot.battery}%`
    );

    setRobotsData(newRobotsState);
    setIsBusy(false);
  };

  // Обробка вибору робота
  const handleSelectRobot = (e) => {
    setSelectedRobotId(e.target.value);
  };

  return (
    <>
      <Navbar />
      <h1>Система керування роботом</h1>
      <Routes>
        <Route
          path="/"
          element={
            <DashboardPage
              robotsData={robotsData}
              selectedRobotId={selectedRobotId}
              isLoading={isLoading}
              isBusy={isBusy}
              handleCommand={handleCommand}
              handleSelectRobot={handleSelectRobot}
            />
          }
        />
        <Route path="/log" element={<LogPage logs={logs} />} />
      </Routes>
    </>
  );
}

export default App;
