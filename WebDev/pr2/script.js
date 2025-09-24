let display = document.getElementById("display");
const operators = ["+", "-", "*", "/"];

function append(value) {
  const lastChar = display.value.slice(-1);

  // Якщо поточне значення — оператор
  if (operators.includes(value)) {
    // Якщо останній символ — теж оператор, не додаємо
    if (operators.includes(lastChar)) {
      return;
    }
  }

  display.value += value;
}

function clearDisplay() {
  display.value = "";
}

function calculate() {
  try {
    let result = eval(display.value);
    if (result === Infinity || result === -Infinity) {
      display.value = "Ділення на 0";
    } else {
      display.value = result;
    }
  } catch {
    display.value = "Помилка";
  }
}

// Обробка клавіатурних подій
document.addEventListener("keydown", function (e) {
  const key = e.key;
  if ("0123456789+-*/".includes(key)) {
    append(key);
  } else if (key === "Enter") {
    calculate();
  } else if (key === "Backspace") {
    display.value = display.value.slice(0, -1);
  } else if (key === "Escape") {
    clearDisplay();
  }
});

// Підсвічування кнопок при натисканні
document.querySelectorAll(".buttons button").forEach((btn) => {
  btn.addEventListener("click", () => {
    btn.classList.add("active");
    setTimeout(() => btn.classList.remove("active"), 100);
  });
});
