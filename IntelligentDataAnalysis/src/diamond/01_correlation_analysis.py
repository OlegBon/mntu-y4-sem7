import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr, shapiro
from datetime import datetime
import os

print("Старт")

# Налаштування шляхів
DATA_FILE = os.path.join("data", "diamond", "diamonds_dataset.csv")
RESULTS_DIR = os.path.join("results", "diamond")

# Визначаємо імена файлів для результатів
HIST_PLOT_FILE = "01_correlation_analysis_histograms.png"
SCATTER_PLOT_FILE = "01_correlation_analysis_scatterplot.png"
REPORT_FILE = "01_correlation_analysis_report.md"

# Створюємо повні шляхи
HIST_PLOT_PATH = os.path.join(RESULTS_DIR, HIST_PLOT_FILE)
SCATTER_PLOT_PATH = os.path.join(RESULTS_DIR, SCATTER_PLOT_FILE)
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

# Задаємо змінні для аналізу
x = df['carat_weight']
y = df['price']
x_name = "Вага (carat_weight)"
y_name = "Ціна (price)"

print(f"Дані завантажено. Аналізуємо зв'язок між: {x_name} та {y_name}")


# Візуалізація - гістограми
print(f"Збереження гістограм у {HIST_PLOT_PATH}")
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
sns.histplot(x, kde=True, color='skyblue')
plt.title(f"Гістограма {x_name}")

plt.subplot(1, 2, 2)
sns.histplot(y, kde=True, color='salmon')
plt.title(f"Гістограма {y_name}")

plt.tight_layout()
plt.savefig(HIST_PLOT_PATH)
plt.close()

# Візуалізація - діаграма розсіювання
print(f"Збереження діаграми розсіювання у {SCATTER_PLOT_PATH}")
plt.figure(figsize=(8, 6))
# Додаємо alpha=0.5, оскільки у нас 1000 точок, щоб бачити щільність
sns.scatterplot(x=x, y=y, data=df, alpha=0.5) 
plt.title(f"Діаграма розсіювання {y_name} vs {x_name}")
plt.xlabel(x_name)
plt.ylabel(y_name)
plt.grid(True)
plt.savefig(SCATTER_PLOT_PATH)
plt.close()

# Статистичний аналіз кореляції
print("Проведення тесту Шапіро-Уілка на нормальність")
# Тест Шапіро-Уілка
stat_x, p_x = shapiro(x)
stat_y, p_y = shapiro(y)

print(f"Shapiro-Wilk {x_name}: p={p_x:.4e}")
print(f"Shapiro-Wilk {y_name}: p={p_y:.4e}")

# Вибір методу кореляції
if p_x > 0.05 and p_y > 0.05:
    method = 'Пірсон'
    corr, pval = pearsonr(x, y)
    normality_conclusion = "Обидві змінні розподілені нормально (p > 0.05)."
else:
    method = 'Спірмен'
    corr, pval = spearmanr(x, y)
    normality_conclusion = "Принаймні одна зі змінних не розподілена нормально (p < 0.05)."

print(f"Обраний метод кореляції: {method}")
print(f"Коефіцієнт кореляції: {corr:.4f}")
print(f"p-value: {pval:.4e}")

# Визначення сили та напрямку кореляції
if abs(corr) < 0.3:
    strength = 'слабкий'
elif abs(corr) < 0.7:
    strength = 'середній'
else:
    strength = 'сильний'

direction = 'прямий' if corr > 0 else 'обернений'
print(f"Тип зв’язку: {direction}, сила: {strength}")

# Генерація звіту
print(f"Генерація звіту у {REPORT_PATH}")
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(f"# Звіт з Самостійної роботи №1: Кореляційний аналіз\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write(f"**Предметна область:** Ідентифікація діамантів (diamonds_dataset.csv)\n")
    f.write(f"**Мета:** Визначити тип та тісноту взаємозв’язку між змінними `{x_name}` та `{y_name}`.\n\n")
    f.write("---\n\n")

    f.write("## 1. Аналіз розподілу даних\n\n")
    f.write(f"![Гістограми розподілу]({HIST_PLOT_FILE})\n\n")
    f.write("**Перевірка на нормальність (Тест Шапіро-Уілка):**\n")
    f.write(f"* `{x_name}`: p-value = {p_x:.4e}\n")
    f.write(f"* `{y_name}`: p-value = {p_y:.4e}\n\n")
    f.write(f"**Висновок:** {normality_conclusion}\n")

    f.write("\n## 2. Аналіз кореляційного зв'язку\n\n")
    f.write(f"![Діаграма розсіювання]({SCATTER_PLOT_FILE})\n\n")
    f.write("**Результати розрахунку:**\n\n")
    f.write(f"- **Обраний метод:** {method} (оскільки дані не є нормальними).\n")
    f.write(f"- **Коефіцієнт кореляції (r):** `{corr:.4f}`\n")
    f.write(f"- **p-value:** `{pval:.4e}`\n\n")
    
    f.write("## 3. Загальний висновок\n\n")
    
    pval_desc = "статистично значущим (p < 0.001)" if pval < 0.001 else f"статистично значущим (p = {pval:.4f})"
    
    f.write(f"Між `{x_name}` та `{y_name}` існує **{strength} {direction} зв’язок**.\n\n")
    f.write(f"Зв'язок є {pval_desc}, що дозволяє відхилити нульову гіпотезу про відсутність кореляції. "
            "Це підтверджує нашу закладену в генератор логіку, що ціна діаманта сильно залежить від його ваги.\n")

print(f"\nЗвіт збережено: {REPORT_PATH}")