const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Початкові дані про роботів
export const fetchRobotsData = async () => {
  console.log("Виконую fetch-запит до /robots.json...");
  await delay(1500);
  const response = await fetch("/robots.json");
  const data = await response.json();
  return data;
};

// Функція для обчислення відстані між двома точками
const calculateDistance = (pos1, pos2) => {
  // Теорема Піфагора
  return Math.sqrt(Math.pow(pos2.x - pos1.x, 2) + Math.pow(pos2.y - pos1.y, 2));
};

// Функція для "відправки" команди роботу (імітація API виклику)
// Приймає всіх роботів і ID активного робота
export const sendRobotCommand = (command, allRobots, activeRobotId) => {
  return new Promise((resolve) => {
    // console.log(`Команда '${command}' для робота ${activeRobotId}`);
    const LOW_BATTERY_THRESHOLD = 30;

    // Використовуємо .map() для створення нового масиву
    const newRobotsArray = allRobots.map((robot) => {
      // Якщо це не той робот, якого ми чіпаємо, повертаємо його без змін
      if (robot.id !== activeRobotId) {
        return robot;
      }

      // Обробка команди для активного робота
      let currentCommand = command;
      if (
        command === "start-mission" &&
        robot.battery < LOW_BATTERY_THRESHOLD
      ) {
        console.log("Заряд низький! Примусове повернення.");
        currentCommand = "return-to-base";
      }

      let newState = { ...robot };
      let distance = 0;

      if (currentCommand === "start-mission") {
        const newX = Math.floor(Math.random() * (600 - 40));
        const newY = Math.floor(Math.random() * (400 - 40));
        const newPos = { x: newX, y: newY };
        distance = calculateDistance(robot.position, newPos);
        newState = { ...robot, status: "Moving", position: newPos };
      } else if (currentCommand === "return-to-base") {
        distance = calculateDistance(robot.position, robot.basePosition);
        newState = {
          ...robot,
          status: "Charging",
          position: robot.basePosition,
        };
      }

      // Логіка батареї
      const batteryDrain = distance * 0.1;
      let newBattery = Math.max(0, robot.battery - batteryDrain);

      if (currentCommand === "return-to-base") {
        if (distance > 0) console.log("Прибув на базу. Зарядка...");
        newBattery = 100;
      }

      newState.battery = Math.round(newBattery);
      return newState; // Повертаємо оновлений об'єкт робота
    });

    // Імітуємо затримку
    setTimeout(() => {
      resolve({ success: true, newRobotsState: newRobotsArray });
    }, 500);
  });
};
