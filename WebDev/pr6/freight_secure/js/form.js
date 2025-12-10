// Логіка активації кнопки тільки при змінах
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("editForm");
  // Якщо форми немає на сторінці (наприклад, це create.php), нічого не робимо
  if (!form) return;

  const btn = document.getElementById("saveBtn");
  const inputs = form.querySelectorAll("input, textarea, select");
  const initialValues = {};

  // Запам'ятовуємо початкові значення
  inputs.forEach((input) => {
    if (input.name) {
      initialValues[input.name] = input.value;
    }
  });

  // Функція перевірки
  function checkChanges() {
    let hasChanges = false;
    inputs.forEach((input) => {
      // Порівнюємо з початковим значенням і встановлюємо активність кнопки
      if (input.name && input.value !== initialValues[input.name]) {
        hasChanges = true;
      }
    });
    btn.disabled = !hasChanges;
  }

  // Слухаємо події
  inputs.forEach((input) => {
    input.addEventListener("input", checkChanges);
    input.addEventListener("change", checkChanges);
  });

  // Блокування кнопки при відправці (Fix)
  form.addEventListener("submit", function () {
    // Використовуємо setTimeout, щоб форма встигла "полетіти" на сервер
    setTimeout(() => {
      btn.innerText = "Збереження...";
      btn.disabled = true;
    }, 0);
  });
});
