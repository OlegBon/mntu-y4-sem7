import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from datetime import datetime
import os

print("Старт")

# Налашттування шляхів
DATA_FILE = os.path.join("data", "diamond", "diamonds_dataset.csv")
RESULTS_DIR = os.path.join("results", "diamond")

# Визначаємо імена файлів для результатів
PLOT_FILE = "02_linear_regression_plot.png"
REPORT_FILE = "02_linear_regression_report.md"

# Створюємо повні шляхи
PLOT_PATH = os.path.join(RESULTS_DIR, PLOT_FILE)
REPORT_PATH = os.path.join(RESULTS_DIR, REPORT_FILE)

# Створення папки для результатів, якщо її не існує
os.makedirs(RESULTS_DIR, exist_ok=True)


# Завантаження даних
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"ПОМИЛКА: Файл {DATA_FILE} не знайдено.")
    print("Будь ласка, спочатку запустіть скрипт '00_generate_dataset.py'")
    exit()

# Для лінійної регресії X має бути 2D-масивом
X = df[['carat_weight']] 
y = df['price']
x_name = "Вага (carat_weight)"
y_name = "Ціна (price)"

print(f"Дані завантажено. Будуємо модель: {y_name} ~ {x_name}")


# Побудова моделі лінійної регресії
# Створюємо та навчаємо модель лінійної регресії
model = LinearRegression()
model.fit(X, y)

# Отримуємо коефіцієнти
b1 = model.coef_[0] # Коефіцієнт нахилу (beta_1)
b0 = model.intercept_ # Вільний член (beta_0)
model_formula = f"Y = {b1:.2f} * X + {b0:.2f}"

# Отримуємо прогноз
y_pred = model.predict(X)

# Оцінюємо якість моделі
r2 = r2_score(y, y_pred)
print(f"Модель побудовано: {model_formula}")
print(f"Коефіцієнт детермінації R²: {r2:.4f}")


# Візуалізація результатів
print(f"Збереження графіка у {PLOT_PATH}")
plt.figure(figsize=(10, 6))
# Діаграма розсіювання (як у СР-1)
sns.scatterplot(x=X['carat_weight'], y=y, alpha=0.5, label='Фактичні дані (1000 шт.)')
# Лінія регресії
plt.plot(X, y_pred, color='red', linewidth=2, label=f'Лінійна модель (R²={r2:.3f})')
plt.title(f"Лінійна регресія: {y_name} ~ {x_name}")
plt.xlabel(x_name)
plt.ylabel(y_name)
plt.legend()
plt.grid(True)
plt.savefig(PLOT_PATH)
plt.close()

# Генерація звіту
print(f"Генерація звіту у {REPORT_PATH}")
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(f"# Звіт з Самостійної роботи №2: Лінійний регресійний аналіз\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write(f"**Предметна область:** Ідентифікація діамантів (diamonds_dataset.csv)\n")
    f.write(f"**Мета:** Навчитись будувати лінійну регресійну модель між залежною (`{y_name}`) та незалежною (`{x_name}`) змінними.\n\n")
    f.write("---\n\n")

    f.write("## 1. Результати моделювання\n\n")
    f.write("Побудовано лінійну регресійну модель за методом найменших квадратів (OLS).\n\n")
    f.write(f"- **Залежна змінна (Y):** {y_name}\n")
    f.write(f"- **Незалежна змінна (X):** {x_name}\n")
    f.write(f"- **Отримане рівняння регресії:** `{model_formula}`\n")
    f.write(f"- **Коефіцієнт детермінації ($R^2$):** `{r2:.4f}`\n\n")

    f.write("## 2. Візуалізація моделі\n\n")
    f.write(f"![Графік лінійної регресії]({PLOT_FILE})\n\n")
    
    f.write("## 3. Висновок\n\n")
    f.write(f"Коефіцієнт детермінації $R^2$ показує, що побудована лінійна модель пояснює приблизно **{r2:.1%}** варіації у ціні діаманта.\n\n")
    f.write("Як видно з графіка, лінійна модель лише частково описує зв'язок. Дані мають чітко виражений **нелінійний (експоненціальний)** характер: "
            "ціна зростає набагато швидше, ніж вага. "
            "Ця модель є **базовою (baseline)** і буде використана для порівняння з більш складними нелінійними моделями в Cамостійній роботі №3.\n")

print(f"\nЗвіт збережено: {REPORT_PATH}")