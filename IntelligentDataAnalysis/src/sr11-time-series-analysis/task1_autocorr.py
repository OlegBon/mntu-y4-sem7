import numpy as np
import matplotlib.pyplot as plt
import os

# Налаштування, вхідні дані
y = [1.6, 0.8, 1.2, 0.5, 0.9, 1.1, 1.1, 0.6, 1.5, 0.8, 0.9, 1.2, 0.5, 1.3, 0.8, 1.2]
RESULTS_DIR = "results/sr11-time-series-analysis"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Побудова графіка часового ряду
def plot_time_series(y):
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(y)+1), y, marker='o', linestyle='-')
    plt.title("Часовий ряд (16 спостережень)")
    plt.xlabel("t")
    plt.ylabel("y(t)")
    plt.grid(True)
    filename = "task1_autocorr_series.png"
    plt.savefig(os.path.join(RESULTS_DIR, filename))
    plt.close()
    return filename

# Побудова графіка y(t+1) vs y(t)
def plot_lagged_scatter(y):
    yt = y[:-1]
    yt1 = y[1:]
    plt.figure(figsize=(6, 6))
    plt.scatter(yt, yt1, color='darkblue')
    plt.title("Залежність y(t+1) від y(t)")
    plt.xlabel("y(t)")
    plt.ylabel("y(t+1)")
    plt.grid(True)
    filename = "task1_autocorr_lagged.png"
    plt.savefig(os.path.join(RESULTS_DIR, filename))
    plt.close()
    return filename

# Обчислення коефіцієнта автокореляції першого порядку
def compute_autocorrelation(y):
    yt = np.array(y[:-1])
    yt1 = np.array(y[1:])
    r = np.corrcoef(yt, yt1)[0, 1]
    return round(r, 4)

# Перевірка обчислення
# print(f"Коефіцієнт автокореляції першого порядку r₁: {np.corrcoef(np.array(y[:-1]), np.array(y[1:]))[0, 1]:.4f}")

# Генерація звіту
def generate_report(series_img, lagged_img, r_value):
    report_path = os.path.join(RESULTS_DIR, "task1_autocorr.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"""# Самостійна робота №11 — Аналіз часового ряду (Задача 1)

## Вхідні дані
Часовий ряд з 16 спостережень:
`{y}`

## a) Графік часового ряду
![Графік ряду]({series_img})

## b) Наближена оцінка r₁ з графіка ряду
Візуальний аналіз графіка часового ряду показує часті коливання "вгору-вниз" (наприклад, 1.6 → 0.8, 1.2 → 0.5), що свідчить про ймовірну **від'ємну автокореляцію** першого порядку.

## c) Графік залежності y(t+1) від y(t) та точний r₁
Графік залежності $y(t+1)$ від $y(t)$ наочно демонструє структуру автокореляції:

![Графік лагової залежності]({lagged_img})

Хмара точок витягнута з верхнього лівого кута в нижній правий, що візуально підтверджує наявність **від'ємної кореляції**.

**Точний розрахунок коефіцієнта автокореляції першого порядку:**
$r_1 = {r_value:.4f}$

## Висновок
Графічний аналіз та точний розрахунок узгоджуються: часовий ряд демонструє **помірну від'ємну автокореляцію** першого порядку ($r_1 \\approx -0.64$). Це означає, що високі значення ряду мають тенденцію змінюватися низькими, і навпаки. Цю властивість слід враховувати при виборі та побудові прогнозної моделі для даного ряду.
""")
    print(f"Звіт збережено: {report_path}")

# (Решта коду залишається без змін)

# Основний блок
if __name__ == "__main__":
    print("Аналіз часового ряду...")
    img_series = plot_time_series(y)
    img_lagged = plot_lagged_scatter(y)
    r = compute_autocorrelation(y)
    # Передаємо 'y' у функцію звіту, щоб вивести дані
    generate_report(img_series, img_lagged, r) 
    print("Завершено.")
