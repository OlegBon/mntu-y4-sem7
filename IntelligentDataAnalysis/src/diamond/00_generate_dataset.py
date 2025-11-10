import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

print("Початок генерації набору даних (v2)...")

# Налаштування
NUM_ROWS = 1000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31) # Дата кінця періоду сертифікації
# TODAY = datetime.now() # "Сьогодні" для розрахунку цензурованих даних
TODAY = END_DATE # "Сьогодні" - це дата нашого зрізу даних

OUTPUT_DIR = "data/diamond"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "diamonds_dataset.csv")

# Словники кодування (згідно з IDC IDC-Rules_ 2013 (July).pdf)
STONE_ORIGIN_MAP = {1: 'Natural', 2: 'Treated', 3: 'Synthetic', 0: 'Simulant'}
COLOR_MAP = {1: 'D', 2: 'E', 3: 'F', 4: 'G', 5: 'H', 6: 'I', 7: 'J', 8: 'K', 9: 'L', 10: 'M-Z'}
CLARITY_MAP = {1: 'IF', 2: 'VVS1', 3: 'VVS2', 4: 'VS1', 5: 'VS2', 6: 'SI1', 7: 'SI2', 8: 'P1', 9: 'P2', 10: 'P3'}
CUT_MAP = {1: 'Excellent', 2: 'Very Good', 3: 'Good', 4: 'Fair'}
FLUORESCENCE_MAP = {1: 'Nil', 2: 'Slight', 3: 'Medium', 4: 'Strong'}
EXPERT_MAP = {1: 'Expert_1', 2: 'Expert_2', 3: 'Expert_3', 4: 'Expert_4', 5: 'Expert_5'}
SENTIMENT_MAP = {1: 'Positive', 0: 'Neutral', -1: 'Negative'}

# Створення папки, якщо її не існує
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Генерація випадкових дат
def random_dates(start, end, n):
    total_days = (end - start).days
    random_days = np.random.randint(0, total_days, n)
    return [start + timedelta(days=int(d)) for d in random_days]

# Генерація основних даних
# Створюємо вагу (carat_weight)
carat_weight = np.round(np.random.lognormal(mean=-0.3, sigma=0.4, size=NUM_ROWS), 2)
carat_weight = np.clip(carat_weight, 0.2, 5.0) 

data = {
    # Блок 1: Фізичні характеристики
    'carat_weight': carat_weight,
    'color_grade': np.random.choice(list(COLOR_MAP.keys()), NUM_ROWS, p=[0.05, 0.1, 0.15, 0.2, 0.2, 0.1, 0.1, 0.05, 0.03, 0.02]),
    'clarity_grade': np.random.choice(list(CLARITY_MAP.keys()), NUM_ROWS, p=[0.05, 0.1, 0.15, 0.2, 0.2, 0.1, 0.1, 0.05, 0.03, 0.02]),
    'polish_grade': np.random.choice(list(CUT_MAP.keys()), NUM_ROWS, p=[0.3, 0.4, 0.2, 0.1]),
    'proportions_grade': np.random.choice(list(CUT_MAP.keys()), NUM_ROWS, p=[0.3, 0.4, 0.2, 0.1]),
    'symmetry_grade': np.random.choice(list(CUT_MAP.keys()), NUM_ROWS, p=[0.3, 0.4, 0.2, 0.1]),
    'fluorescence_grade': np.random.choice(list(FLUORESCENCE_MAP.keys()), NUM_ROWS, p=[0.4, 0.3, 0.2, 0.1]),
    'stone_origin': np.random.choice(list(STONE_ORIGIN_MAP.keys()), NUM_ROWS, p=[0.70, 0.05, 0.20, 0.05]), # 70% Natural

    # Блок 4: Мета-дані процесу
    'expert_id': np.random.choice(list(EXPERT_MAP.keys()), NUM_ROWS),
    'evaluation_time_min': np.random.randint(15, 120, size=NUM_ROWS),
    'report_notes_length': np.random.randint(5, 100, size=NUM_ROWS),
    'report_sentiment': np.random.choice(list(SENTIMENT_MAP.keys()), NUM_ROWS, p=[0.3, 0.6, 0.1]),

    # Блок 3: Часовий вимір (Дата сертифікації)
    'report_date': random_dates(START_DATE, END_DATE, NUM_ROWS),
    
    # Блок 2: Цільові змінні (поки порожні)
    'price': 0.0,
    'is_investment_grade': 0,
    'is_report_rejected': 0,
    'is_sold': 0,
    'days_on_market': 0,
    'sale_date': pd.NaT # Порожня дата (Not a Time)
}

df = pd.DataFrame(data)

# Генерація похідних та цільових змінних
print("Обчислення похідних полів (cut_grade, price, etc.)...")

# Обчислюємо 'cut_grade' (Блок 1)
df['cut_grade'] = df[['polish_grade', 'proportions_grade', 'symmetry_grade']].max(axis=1)

# Мультиплікатори для розрахунку ціни
color_multi = {1: 2.0, 2: 1.8, 3: 1.6, 4: 1.4, 5: 1.2, 6: 1.0, 7: 0.9, 8: 0.8, 9: 0.7, 10: 0.5}
clarity_multi = {1: 3.0, 2: 2.5, 3: 2.2, 4: 1.8, 5: 1.5, 6: 1.0, 7: 0.8, 8: 0.6, 9: 0.4, 10: 0.2}
cut_multi = {1: 1.5, 2: 1.2, 3: 1.0, 4: 0.8}

# Генеруємо цільові змінні (Блок 2)
for i, row in df.iterrows():
    # price
    base_price = (row['carat_weight'] ** 1.7) * 4000 
    price = base_price * \
            color_multi[row['color_grade']] * \
            clarity_multi[row['clarity_grade']] * \
            cut_multi[row['cut_grade']]
    price *= np.random.uniform(0.95, 1.05) 
    df.at[i, 'price'] = max(500, round(price, 0))

    # is_investment_grade
    if (row['color_grade'] <= 4 and # G або краще
        row['clarity_grade'] <= 5 and # VS2 або краще
        row['cut_grade'] <= 2 and # Very Good або краще
        row['carat_weight'] >= 1.0):
        df.at[i, 'is_investment_grade'] = 1
    else:
        df.at[i, 'is_investment_grade'] = 0

    # is_report_rejected
    if (row['expert_id'] == 5 and random.random() < 0.2) or (row['evaluation_time_min'] < 20 and random.random() < 0.1):
        df.at[i, 'is_report_rejected'] = 1
    else:
        df.at[i, 'is_report_rejected'] = 0
        
    # is_sold та days_on_market (для Регресії Кокса)
    # Припустимо, 70% продано, 30% ще ні
    df.at[i, 'is_sold'] = 1 if random.random() < 0.7 else 0 
    
    # Чим краща якість, тим швидше продається (менше днів)
    quality_score = row['color_grade'] + row['clarity_grade'] + row['cut_grade']
    
    if df.at[i, 'is_sold'] == 1:
        # Продано: генеруємо час продажу
        mean_days = max(10, quality_score * 5) 
        days_to_sell = int(np.random.normal(loc=mean_days, scale=30))
        days_to_sell = max(1, days_to_sell) # Mіn 1 день
        
        df.at[i, 'days_on_market'] = days_to_sell
        df.at[i, 'sale_date'] = row['report_date'] + timedelta(days=days_to_sell)
    else:
        # Не продано (цензурування): час спостереження = від дати звіту до сьогодні
        days_observed = (TODAY - row['report_date']).days
        df.at[i, 'days_on_market'] = max(1, days_observed) # Як мінімум 1 день спостереження
        # df.at[i, 'sale_date'] залишається NaT

# Створення report_id та збереження файлу
print("Створення report_id та збереження файлу...")

# Створюємо report_id за маскою 'DR-00001'
report_ids = [f"DR-{i:05d}" for i in range(1, NUM_ROWS + 1)]
df.insert(0, 'report_id', report_ids)

# Перевірка та впорядкування стовпців (додали report_date)
final_columns = [
    'report_id', 'report_date',
    # Блок 1
    'carat_weight', 'color_grade', 'clarity_grade', 'polish_grade', 
    'proportions_grade', 'symmetry_grade', 'cut_grade', 
    'fluorescence_grade', 'stone_origin',
    # Блок 4
    'expert_id', 'evaluation_time_min', 'report_notes_length', 'report_sentiment',
    # Блок 2
    'price', 'is_investment_grade', 'is_report_rejected', 
    'is_sold', 'days_on_market', 'sale_date'
]
df = df[final_columns]

# Збереження у CSV
df.to_csv(OUTPUT_FILE, index=False, date_format='%Y-%m-%d')

print("\nГенерація набору даних завершена!")
print(f"Успішно згенеровано {NUM_ROWS} рядків.")
print(f"Файл збережено у: {OUTPUT_FILE}")
print("\nПерші 5 рядків згенерованих даних:")
print(df.head().to_string())