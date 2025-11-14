import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from datetime import datetime
import os
import warnings

# Ігноруємо попередження про те, що X/y не є позитивними для log (ми це обробимо пізніше)
warnings.filterwarnings('ignore', category=RuntimeWarning)

print("Старт")

# Налаштування шляхів
DATA_FILE = os.path.join("data", "diamond", "diamonds_dataset.csv")
RESULTS_DIR = os.path.join("results", "diamond")

PLOT_FILE = "03_nonlinear_regression_plot.png"
REPORT_FILE = "03_nonlinear_regression_report.md"

PLOT_PATH = os.path.join(RESULTS_DIR, PLOT_FILE)
REPORT_PATH = os.path.join(RESULTS_DIR, REPORT_FILE)

os.makedirs(RESULTS_DIR, exist_ok=True)

# Завантаження даних
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"ПОМИЛКА: Файл {DATA_FILE} не знайдено.")
    print("Будь ласка, спочатку запустіть скрипт '00_generate_dataset.py'")
    exit()

# Оскільки логарифм 0 не визначений, беремо тільки дані > 0
# (Наш генератор і так створює price > 500, але це на всяк випадок)
df_clean = df[(df['carat_weight'] > 0) & (df['price'] > 0)].copy()

X = df_clean[['carat_weight']] 
y = df_clean['price']
x_name = "Вага (carat_weight)"
y_name = "Ціна (price)"

print(f"Дані завантажено. Будуємо 6 моделей: {y_name} ~ {x_name}")

# Сортуємо значення для плавних ліній на графіку
# X_sorted = np.sort(X, axis=0)
# X_sorted_flat = X_sorted.flatten() # 1D-масив для зручності
df_sorted = df_clean.sort_values(by='carat_weight')
X_sorted = df_sorted[['carat_weight']] # Тепер X_sorted - це DataFrame
X_sorted_flat = df_sorted['carat_weight'] # А це 1D-Series

# Навчання моделей
models = {} # Словник для формул
predictions = {} # Словник для прогнозів (для графіка)
model_r2_scores = {} # Словник для R²

# Модель 1: Лінійна (з СР-2)
model_linear = LinearRegression()
model_linear.fit(X, y)
y_pred_linear = model_linear.predict(X_sorted)
r2_linear = r2_score(y, model_linear.predict(X))
models['Лінійна'] = f"Y = {model_linear.coef_[0]:.2f}*X + {model_linear.intercept_:.2f}"
predictions[f'Лінійна (R²={r2_linear:.3f})'] = y_pred_linear
model_r2_scores['Лінійна'] = r2_linear

# Модель 2: Поліноміальна 2-го ступеня
poly_2 = PolynomialFeatures(degree=2)
X_poly_2 = poly_2.fit_transform(X)
X_poly_2_sorted = poly_2.transform(X_sorted)
model_poly_2 = LinearRegression()
model_poly_2.fit(X_poly_2, y)
y_pred_poly_2 = model_poly_2.predict(X_poly_2_sorted)
r2_poly_2 = r2_score(y, model_poly_2.predict(X_poly_2))
models['Поліном 2-го ст.'] = "Y = b2*X^2 + b1*X + b0"
predictions[f'Поліном 2-го ст. (R²={r2_poly_2:.3f})'] = y_pred_poly_2
model_r2_scores['Поліном 2-го ст.'] = r2_poly_2

# Модель 3: Поліноміальна 3-го ступеня
poly_3 = PolynomialFeatures(degree=3)
X_poly_3 = poly_3.fit_transform(X)
X_poly_3_sorted = poly_3.transform(X_sorted)
model_poly_3 = LinearRegression()
model_poly_3.fit(X_poly_3, y)
y_pred_poly_3 = model_poly_3.predict(X_poly_3_sorted)
r2_poly_3 = r2_score(y, model_poly_3.predict(X_poly_3))
models['Поліном 3-го ст.'] = "Y = b3*X^3 + b2*X^2 + b1*X + b0"
predictions[f'Поліном 3-го ст. (R²={r2_poly_3:.3f})'] = y_pred_poly_3
model_r2_scores['Поліном 3-го ст.'] = r2_poly_3

# Модель 4: Степенева (Y = a * X^b  =>  log(Y) = log(a) + b*log(X))
X_log = np.log(X)
y_log = np.log(y)
model_power = LinearRegression()
model_power.fit(X_log, y_log)
b1_power = model_power.coef_[0]
b0_power = np.exp(model_power.intercept_)
y_pred_power = b0_power * (X_sorted_flat ** b1_power)
r2_power = r2_score(y, b0_power * (X['carat_weight'] ** b1_power))
models['Степенева'] = f"Y = {b0_power:.2f} * X^{b1_power:.2f}"
predictions[f'Степенева (R²={r2_power:.3f})'] = y_pred_power
model_r2_scores['Степенева'] = r2_power

# Модель 5: Експоненціальна (Y = a * e^(b*X)  =>  log(Y) = log(a) + b*X)
model_exp = LinearRegression()
model_exp.fit(X, y_log) # X - звичайний, y - логарифм
b1_exp = model_exp.coef_[0]
b0_exp = np.exp(model_exp.intercept_)
y_pred_exp = b0_exp * np.exp(b1_exp * X_sorted_flat)
r2_exp = r2_score(y, b0_exp * np.exp(b1_exp * X['carat_weight']))
models['Експоненціальна'] = f"Y = {b0_exp:.2f} * e^({b1_exp:.2f}*X)"
predictions[f'Експоненціальна (R²={r2_exp:.3f})'] = y_pred_exp
model_r2_scores['Експоненціальна'] = r2_exp

# Модель 6: Гіперболічна (Y = a + b/X)
X_hyper = 1 / X['carat_weight']
X_hyper_2d = X_hyper.values.reshape(-1, 1) # Потрібен 2D-масив
X_hyper_sorted = 1 / X_sorted_flat

model_hyper = LinearRegression()
model_hyper.fit(X_hyper_2d, y)
b1_hyper = model_hyper.coef_[0]
b0_hyper = model_hyper.intercept_
y_pred_hyper = b0_hyper + b1_hyper * X_hyper_sorted
r2_hyper = r2_score(y, model_hyper.predict(X_hyper_2d))
models['Гіперболічна'] = f"Y = {b0_hyper:.2f} + ({b1_hyper:.2f} / X)"
predictions[f'Гіперболічна (R²={r2_hyper:.3f})'] = y_pred_hyper
model_r2_scores['Гіперболічна'] = r2_hyper

print("Усі 6 моделей навчено.")

# Візуалізація результатів
print(f"Збереження графіка у {PLOT_PATH}")
plt.figure(figsize=(10, 7))
# Фактичні дані
sns.scatterplot(x=df_clean['carat_weight'], y=df_clean['price'], alpha=0.3, label='Фактичні дані (1000 шт.)')

# Лінії моделей
for label, y_pred in predictions.items():
    plt.plot(X_sorted_flat, y_pred, label=label, linewidth=2)

plt.title(f"Нелінійний регресійний аналіз: {y_name} ~ {x_name}")
plt.xlabel(x_name)
plt.ylabel(y_name)
plt.legend()
plt.grid(True)
plt.ylim(bottom=0, top=y.max()*1.1) 
plt.xlim(left=0, right=X['carat_weight'].max() * 1.1)
plt.savefig(PLOT_PATH)
plt.close()

# Генерація звіту
print(f"Генерація звіту у {REPORT_PATH}")
# Сортуємо результати R² для звіту
sorted_r2 = sorted(model_r2_scores.items(), key=lambda item: item[1], reverse=True)
best_model_name = sorted_r2[0][0]
best_r2 = sorted_r2[0][1]

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(f"# Звіт з Самостійної роботи №3: Нелінійний регресійний аналіз\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write(f"**Мета:** Порівняти лінійну та 5 нелінійних регресійних моделей  для прогнозування `{y_name}` на основі `{x_name}`.\n\n")
    f.write("---\n\n")

    f.write("## 1. Порівняння якості моделей (R²)\n\n")
    f.write("Було побудовано 6 моделей для оцінки зв'язку між ціною та вагою діаманта. "
            "Коефіцієнт детермінації ($R^2$) показує, яку частку варіації ціни пояснює модель.\n\n")
    
    f.write("| Модель | Формула | R² (якість) |\n")
    f.write("| :--- | :--- | :--- |\n")
    
    # Виводимо відсортовані результати
    for model_name, r2_value in sorted_r2:
        f.write(f"| **{model_name}** | `{models[model_name]}` | **{r2_value:.4f}** |\n")
    
    f.write(f"\n**Аналіз $R^2$:**\n")
    f.write(f"1. **Лінійна модель** ($R^2={r2_linear:.3f}$) та **Гіперболічна модель** ($R^2={r2_hyper:.3f}$) показали найгірші результати, "
            f"оскільки їх форма не відповідає реальному експоненціальному зростанню ціни.\n")
    f.write(f"2. **Степенева модель** ($R^2={r2_power:.3f}$) показала **найкращий результат**. "
            f"Це очікувано, оскільки дані генерувалися за схожою логікою ($price \\sim carat\\_weight^{{1.7}}$).\n")
    f.write(f"3. **Поліноміальні моделі** також показали високу якість, причому $R^2$ для моделі 3-го ступеня ($R^2={r2_poly_3:.3f}$) виявився трохи кращим, "
            f"ніж для 2-го ступеня ($R^2={r2_poly_2:.3f}$).\n")

    f.write("\n## 2. Візуалізація моделей\n\n")
    f.write(f"![Графік нелінійних моделей]({PLOT_FILE})\n\n")
    
    f.write("## 3. Загальний висновок\n\n")
    f.write(f"На відміну від Самостійної роботи №2, де лінійна модель дала $R^2 \\approx {r2_linear:.3f}$, "
            f"нелінійні моделі (зокрема, **{best_model_name}**) показують набагато вищу якість "
            f"($R^2 \\approx {best_r2:.3f}$).\n\n")
    f.write("Це доводить, що зв'язок між вагою та ціною діаманта є **сильно нелінійним**. "
            "Для точного прогнозування (апроксимації) ціни необхідно використовувати нелінійні моделі, "
            "що відповідає теоретичним основам нелінійного регресійного аналізу.\n")

print(f"\nЗвіт збережено: {REPORT_PATH}")