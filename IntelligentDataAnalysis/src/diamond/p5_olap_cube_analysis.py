import pandas as pd
import numpy as np
import os
from datetime import datetime

print("Старт")

# Налаштування шляхів до файлів
DATA_FILE = os.path.join("data", "diamond", "diamonds_dataset.csv")
RESULTS_DIR = os.path.join("results", "diamond")
REPORT_FILE = os.path.join(RESULTS_DIR, "p5_olap_report.md")
CUBE_FILE_CSV = os.path.join(RESULTS_DIR, "p5_olap_cube.csv")

# Створення папки для результатів, якщо її не існує
os.makedirs(RESULTS_DIR, exist_ok=True)

# Завантаження "Вітрини Даних"
try:
    df = pd.read_csv(DATA_FILE)
    print("Дані успішно завантажено.")
except FileNotFoundError:
    print(f"ПОМИЛКА: Файл {DATA_FILE} не знайдено.")
    print("Будь ласка, спочатку запустіть скрипт '00_generate_dataset.py'")
    exit()

# Підготовка даних для OLAP-куба (визначення Вимірів)
print("Підготовка вимірів (Dimensions)")
# Перетворюємо 'report_date' на тип datetime
df['report_date'] = pd.to_datetime(df['report_date'])

# Створюємо ієрархію для часу (Рік -> Квартал -> Місяць)
df['year'] = df['report_date'].dt.year
df['quarter'] = df['report_date'].dt.quarter
df['month'] = df['report_date'].dt.month

# Словники для читабельності
STONE_ORIGIN_MAP = {1: 'Natural', 2: 'Treated', 3: 'Synthetic', 0: 'Simulant'}
EXPERT_MAP = {1: 'Expert_1', 2: 'Expert_2', 3: 'Expert_3', 4: 'Expert_4', 5: 'Expert_5'}

# Мапуємо ID на імена для звітів
df['expert_name'] = df['expert_id'].map(EXPERT_MAP)
df['origin_name'] = df['stone_origin'].map(STONE_ORIGIN_MAP)

# Побудова OLAP-куба (groupby плюс agg)
print("Побудова OLAP-куба (групування даних)")

# Визначаємо наші Виміри (Dimensions)
# 5 вимірів, 3 з яких ієрархічні (Year -> Quarter -> Month)
dimensions = ['year', 'quarter', 'month', 'expert_name', 'origin_name']

# Обчислюємо Міри (Measures)
olap_cube = df.groupby(dimensions).agg(
    Average_Price=('price', 'mean'), # Міра 1
    Total_Sold_Count=('is_sold', 'sum'), # Міра 2
    Avg_Days_On_Market=('days_on_market', 'mean') # Міра 3
)

# Округлення значень для кращої читабельності
olap_cube = olap_cube.round(2)

# Зберігаємо повний куб у CSV для подальшого аналізу
olap_cube.to_csv(CUBE_FILE_CSV)
print(f"Повний OLAP-куб збережено у: {CUBE_FILE_CSV}")

# Демонстрація OLAP-операцій
print("\nДемонстрація OLAP-операцій")

# 1. Зріз (Slice): "Дані тільки за 2024 рік, по Expert_1"
print("1. Виконуємо Зріз (Slice)")
slice_data = olap_cube.loc[(2024, slice(None), slice(None), 'Expert_1', slice(None)), :]

# 2. Деталізація (Drill-down): "Провалитися з 2023 року в квартали, а з Q1 - в місяці"
print("2. Виконуємо Деталізацію (Drill-down)")
drill_down_year = olap_cube.loc[2023]
drill_down_quarter = olap_cube.loc[(2023, 1)] # Тільки Q1 2023

# 3. Консолідація (Roll-up): "Піднятися з місяців/кварталів до років"
print("3. Виконуємо Консольдацію (Roll-up)")
roll_up_data = df.groupby('year').agg(
    Average_Price=('price', 'mean'),
    Total_Sold_Count=('is_sold', 'sum')
)

# 4. Обертання (Rotate / Pivot): "Показати 'origin_name' у стовпцях"
print("4. Виконуємо Обертання (Rotate)")
# Беремо зріз за 2025 рік і робимо "обертання"
rotated_data = olap_cube.loc[2025]['Average_Price'].unstack(level='origin_name')

# Генерація звіту
print(f"Генерація звіту: {REPORT_FILE}")
with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.write(f"# Звіт з Практичної роботи №5: Побудова OLAP-куба\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write(f"**Мета:** Одержання навичок у створенні простих багатомірних OLAP кубів з використанням Python та `pandas`.\n\n")
    
    f.write("## 1. Побудований OLAP-куб (фрагмент)\n\n")
    f.write("Побудовано куб з 5 вимірами (`year`, `quarter`, `month`, `expert_name`, `origin_name`) "
            "та 3 мірами (`Average_Price`, `Total_Sold_Count`, `Avg_Days_On_Market`).\n\n")
    f.write("```\n")
    f.write(olap_cube.head(10).round(0).to_string())
    f.write("\n```\n\n")
    f.write(f"Повний куб збережено у файл: `{os.path.basename(CUBE_FILE_CSV)}`\n\n")
    
    f.write("## 2. Демонстрація OLAP-операцій\n\n")
    
    f.write("### 2.1. Зріз (Slice)\n\n")
    f.write(f"**Запит:** *'Показати дані тільки за 2024 рік, по Expert_1'* \n\n")
    f.write("```\n")
    try:
        f.write(slice_data.round(0).to_string())
    except NameError:
        f.write("Дані для цього зрізу відсутні.")
    f.write("\n```\n\n")
    
    f.write("### 2.2. Деталізація (Drill-down)\n\n")
    f.write(f"**Запит:** *'Показати дані по Q1 2023 року (з деталізацією по місяцях)'* \n\n")
    f.write("```\n")
    try:
        f.write(drill_down_quarter.round(0).to_string())
    except NameError:
        f.write("Дані для цього зрізу відсутні.")
    f.write("\n```\n\n")

    f.write("### 2.3. Консолідація (Roll-up)\n\n")
    f.write(f"**Запит:** *'Показати загальні показники по роках (агрегація з місяців/кварталів)'* \n\n")
    f.write("```\n")
    f.write(roll_up_data.round(0).to_string())
    f.write("\n```\n\n")

    f.write("### 2.4. Обертання (Rotate / Pivot)\n\n")
    f.write(f"**Запит:** *'Показати середню ціну за 2025 рік, де рядки - Квартал/Місяць/Експерт, а стовпці - Походження каменя'* \n\n")
    f.write("```\n")
    f.write(rotated_data.head(10).round(0).to_string(na_rep='-'))
    f.write("\n```\n\n")

    f.write("## 3. Висновок\n\n")
    f.write("Використання `pandas.groupby()` з багаторівневим індексом дозволяє ефективно "
            "симулювати архітектуру OLAP-куба. Ми успішно створили 5-вимірний куб з 3 мірами "
            "на основі нашої 'Вітрини Даних' (`diamonds_dataset.csv`).\n\n"
            "Було продемонстровано всі ключові OLAP-операції (Slice, Drill-down, Roll-up, Rotate), "
            "що підтверджує гнучкість `pandas` як інструменту для багатовимірного аналізу, "
            "який є альтернативою спеціалізованим серверам на кшталт `icCube`.\n")

print(f"\nЗвіт збережено у: {REPORT_FILE}")