// Логіка активації кнопки тільки при змінах
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("editForm");
  // Якщо форми немає на сторінці (наприклад, це create.php), нічого не робимо
  if (!form) return;

  const btn = document.getElementById("saveBtn");
  const inputs = form.querySelectorAll("input, textarea, select");
  const initialValues = {};

  // 1. Запам'ятовуємо початкові значення
  inputs.forEach((input) => {
    if (input.name) {
      initialValues[input.name] = input.value;
    }
  });

  // 2. Функція перевірки
  function checkChanges() {
    let hasChanges = false;
    inputs.forEach((input) => {
      if (input.name && input.value !== initialValues[input.name]) {
        hasChanges = true;
      }
    });
    btn.disabled = !hasChanges;
  }

  // 3. Слухаємо події
  inputs.forEach((input) => {
    input.addEventListener("input", checkChanges);
    input.addEventListener("change", checkChanges);
  });
});
