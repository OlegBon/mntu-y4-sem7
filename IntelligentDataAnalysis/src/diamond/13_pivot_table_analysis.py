import pandas as pd
import numpy as np
import os
from datetime import datetime

print("Старт")

# Налаштування шляхів до файлів
DATA_FILE = os.path.join("data", "diamond", "diamonds_dataset.csv")
RESULTS_DIR = os.path.join("results", "diamond")
REPORT_FILE = os.path.join(RESULTS_DIR, "13_pivot_table_report.md")

# Створення папки для результатів, якщо її не існує
os.makedirs(RESULTS_DIR, exist_ok=True)

# Завантаження датасету "Вітрини Даних"
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"ПОМИЛКА: Файл {DATA_FILE} не знайдено.")
    print("Будь ласка, спочатку запустіть скрипт '00_generate_dataset.py'")
    exit()

print("Дані завантажено")

# Підготовка даних для аналізу зведених таблиць (Витягання вимірів)
# Перетворюємо 'report_date' на тип datetime
df['report_date'] = pd.to_datetime(df['report_date'])

# Створюємо нові стовпці для ієрархії часу
df['year'] = df['report_date'].dt.year
df['quarter'] = df['report_date'].dt.quarter

# Словники для читабельності (як робили в CР-12)
STONE_ORIGIN_MAP = {1: 'Natural', 2: 'Treated', 3: 'Synthetic', 0: 'Simulant'}
EXPERT_MAP = {1: 'Expert_1', 2: 'Expert_2', 3: 'Expert_3', 4: 'Expert_4', 5: 'Expert_5'}

# Мапуємо ID на імена для звітів
df['expert_name'] = df['expert_id'].map(EXPERT_MAP)
df['origin_name'] = df['stone_origin'].map(STONE_ORIGIN_MAP)

# Побудова зведених таблиць
print("Розрахунок зведених таблиць")

# Таблиця 1 (Річна): Середня ціна (Міра)
# для Експерта (Рядки) у розрізі Року (Стовпці)
pivot_price_by_year = pd.pivot_table(
    df,
    values="price",
    index="expert_name",
    columns="year",
    aggfunc="mean"
)

# Таблиця 2 (Квартальна): Загальна кількість продажів (Міра)
# для Кварталу (Рядки) у розрізі Походження каменя (Стовпці)
pivot_sales_by_quarter = pd.pivot_table(
    df,
    values="is_sold",
    index="quarter",
    columns="origin_name",
    aggfunc="sum"
)

# Генерація звіту
print(f"Генерація звіту: {REPORT_FILE}")
with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.write(f"# Звіт з Самостійної роботи №13: Практика зі зведеними таблицями\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("**Мета:** Освоїти роботу з зведеними таблицями в Python (`pandas.pivot_table`) на прикладі набору даних РГР.\n\n")
    f.write("---")
    
    f.write("\n\n## Таблиця 1: Середня ціна оцінених діамантів ($) за Експертом та Роком\n\n")
    f.write("Ця зведена таблиця аналізує **Міру (Measure)** `AVG(price)` у розрізі **Вимірів (Dimensions)** `expert_name` та `year`.\n\n")
    # .to_markdown() - зручний спосіб конвертувати DataFrame в Markdown
    # floatfmt=",.0f" - форматує числа (напр., 10000.0 -> 10,000)
    f.write(pivot_price_by_year.to_markdown(floatfmt=",.0f"))
    f.write("\n\n**Аналіз:** Таблиця дозволяє швидко оцінити динаміку середньої вартості роботи кожного експерта. "
            "Наприклад, ми можемо побачити, чи зростає середня вартість каменів, що проходять через `Expert_1`, "
            "з року в рік, чи, можливо, `Expert_3` спеціалізується на дорожчих каменях.\n")

    f.write("\n\n---\n\n")
    
    f.write("\n\n## Таблиця 2: Загальна кількість продажів (шт.) за Кварталом та Походженням\n\n")
    f.write("Ця зведена таблиця аналізує **Міру** `SUM(is_sold)` у розрізі **Вимірів** `quarter` та `origin_name`.\n\n")
    f.write(pivot_sales_by_quarter.to_markdown(floatfmt=".0f"))
    f.write("\n\n**Аналіз:** Таблиця демонструє сезонність продажів. "
            "Ми можемо чітко побачити, в які квартали продається найбільше `Natural` діамантів "
            "(очікуємо піки, напр., у 4-му кварталі перед святами) та як розподілені продажі `Synthetic` каменів протягом року.\n")

    f.write("\n\n---\n\n")
    f.write("## Висновок\n\n")
    f.write("Використання `pandas.pivot_table` є прямою реалізацією концепції зведених таблиць. "
            "Цей інструмент дозволяє швидко агрегувати Міри (Measures) (наприклад, price, is_sold) "
            "за різними Вимірами (Dimensions) (expert_name, year, quarter). Ми можемо перетворити 'сиру' "
            "Вітрину Даних (diamonds_dataset.csv) на інтерактивний звіт, придатний для швидкого аналізу та "
            "прийняття бізнес-рішень.\n")

print(f"\nЗвіт збережено у: {REPORT_FILE}")