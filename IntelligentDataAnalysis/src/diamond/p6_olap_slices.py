import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

print("Старт")

# Налаштування шляхів
DATA_FILE = os.path.join("data", "diamond", "diamonds_dataset.csv")
RESULTS_DIR = os.path.join("results", "diamond")
REPORT_FILE = os.path.join(RESULTS_DIR, "p6_olap_slices_report.md")

# Файли для графіків
PLOT_REVENUE = os.path.join(RESULTS_DIR, "p6_slice_revenue.png")
PLOT_EXPERTS = os.path.join(RESULTS_DIR, "p6_slice_experts.png")
PLOT_MATRIX = os.path.join(RESULTS_DIR, "p6_slice_product_matrix.png")

os.makedirs(RESULTS_DIR, exist_ok=True)

# Завантаження та підготовка
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print("ПОМИЛКА: Файл даних не знайдено.")
    exit()

df['report_date'] = pd.to_datetime(df['report_date'])
df['year'] = df['report_date'].dt.year
df['quarter'] = df['report_date'].dt.quarter

# Мапінг
STONE_ORIGIN_MAP = {1: 'Natural', 2: 'Treated', 3: 'Synthetic', 0: 'Simulant'}
EXPERT_MAP = {1: 'Expert_1', 2: 'Expert_2', 3: 'Expert_3', 4: 'Expert_4', 5: 'Expert_5'}
CUT_MAP = {1: 'Excellent', 2: 'Very Good', 3: 'Good', 4: 'Fair'}
COLOR_MAP = {1: 'D', 2: 'E', 3: 'F', 4: 'G', 5: 'H', 6: 'I', 7: 'J', 8: 'K', 9: 'L', 10: 'M-Z'}

df['expert_name'] = df['expert_id'].map(EXPERT_MAP)
df['origin_name'] = df['stone_origin'].map(STONE_ORIGIN_MAP)
df['cut_name'] = df['cut_grade'].map(CUT_MAP)
df['color_name'] = df['color_grade'].map(COLOR_MAP)
df['price_per_carat'] = df['price'] / df['carat_weight']

# Розрахунок OLAP-зрізів

# Зріз 1. Динаміка Виручки (Strategic Slice)
print("1. Розрахунок та візуалізація Виручки")
df_sold = df[df['is_sold'] == 1]
slice_revenue = df_sold.groupby(['year', 'origin_name'])['price'].sum().unstack()

plt.figure(figsize=(10, 6))
slice_revenue.plot(kind='bar', stacked=True, colormap='viridis', ax=plt.gca())
plt.title('Динаміка Виручки за Роками та Походженням')
plt.ylabel('Сума продажів ($)')
plt.xlabel('Рік')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOT_REVENUE)
plt.close()

# Зріз 2. Ефективність (KPI) Експертів (Operational Slice)
print("2. Розрахунок KPI експертів")
slice_experts = df.groupby('expert_name').agg(
    Reports_Count=('report_id', 'count'),
    Avg_Time=('evaluation_time_min', 'mean'),
    Rejection_Rate=('is_report_rejected', 'mean')
).sort_values('Rejection_Rate')

# Візуалізація: Scatterplot (Час vs Відхилення)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=slice_experts, x='Avg_Time', y='Rejection_Rate', size='Reports_Count', sizes=(100, 1000), hue=slice_experts.index)
plt.title('Ефективність Експертів: Час vs Якість')
plt.xlabel('Середній час оцінки (хв)')
plt.ylabel('Відсоток відхилень (Rejection Rate)')
plt.grid(True)
plt.savefig(PLOT_EXPERTS)
plt.close()

# Зріз 3. Продуктова Матриця (Product Slice)
print("3. Розрахунок Продуктової матриці")
df_natural = df[df['stone_origin'] == 1]
slice_product = pd.pivot_table(
    df_natural,
    values='price_per_carat',
    index='color_name',
    columns='cut_name',
    aggfunc='mean'
)
# Сортуємо індекси для логічного порядку
color_order = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M-Z']
cut_order = ['Excellent', 'Very Good', 'Good', 'Fair']
slice_product = slice_product.reindex(index=color_order, columns=cut_order)

# Візуалізація: Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(slice_product, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': 'Ціна за карат ($)'})
plt.title('Матриця цін ($/ct) для Natural Diamonds')
plt.ylabel('Колір (Color)')
plt.xlabel('Огранювання (Cut)')
plt.tight_layout()
plt.savefig(PLOT_MATRIX)
plt.close()

# Генерація звіту
print(f"Генерація звіту: {REPORT_FILE}")
with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.write(f"# Звіт з Практичної роботи №6: Побудова OLAP-зрізів\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("**Мета:** Спроєктувати та реалізувати складні аналітичні зрізи даних для оцінки економічних показників, використовуючи Python.\n\n")
    
    f.write("## 1. Стратегічний зріз: Динаміка Виручки\n")
    f.write("Аналіз суми продажів у розрізі років та типів каменів.\n\n")
    f.write(f"![Графік виручки]({os.path.basename(PLOT_REVENUE)})\n\n")
    f.write("**Табличні дані ($):**\n")
    f.write(slice_revenue.round(0).to_markdown())
    f.write("\n\n")

    f.write("## 2. Операційний зріз: KPI Експертів\n")
    f.write("Аналіз ефективності роботи персоналу (співвідношення швидкості та якості).\n\n")
    f.write(f"![Графік експертів]({os.path.basename(PLOT_EXPERTS)})\n\n")
    f.write("**Табличні дані:**\n")
    f.write(slice_experts.round(3).to_markdown())
    f.write("\n\n")

    f.write("## 3. Продуктовий зріз: Цінова Матриця (Natural)\n")
    f.write("Теплова карта середньої ціни за карат для природних діамантів.\n\n")
    f.write(f"![Теплова карта]({os.path.basename(PLOT_MATRIX)})\n\n")
    f.write("**Табличні дані ($/ct):**\n")
    f.write(slice_product.round(0).to_markdown())
    f.write("\n\n")
    
    f.write("## Висновок\n")
    f.write("У ході роботи було реалізовано три типи OLAP-зрізів (Стратегічний, Операційний, Продуктовий). "
            "Замість використання зовнішніх офісних додатків, було автоматизовано процес побудови аналітичної звітності "
            "безпосередньо в Python, отримавши готові для прийняття рішень візуалізації та таблиці.")

print(f"\nЗвіт збережено у файл: {REPORT_FILE}")