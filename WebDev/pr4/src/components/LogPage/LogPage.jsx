import "./LogPage.css";
import React from "react";

// Отримуємо логи через props
function LogPage({ logs }) {
  return (
    <div>
      <h2>Журнал завдань</h2>

      <div className="log-container">
        {logs.length === 0 ? (
          <p className="log-empty">Журнал порожній. Ще не було жодних дій.</p>
        ) : (
          <ul className="log-list">
            {logs.map((log, index) => (
              <li key={index} className="log-item">
                {log}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default LogPage;
