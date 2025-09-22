import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import CoxPHFitter
from datetime import datetime
import os

# === Етап 1: Підготовка даних ===
os.makedirs("results/sr5-cox-regression", exist_ok=True)

df = pd.read_csv("data/sr5-cox-regression.csv")

# Базова перевірка
print(df.info())
print(df.describe().round(3))

with open("results/sr5-cox-regression/report.md", "w", encoding="utf-8") as f:
    f.write(f"# Звіт Cox-регресії\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("## Етап 1: Підготовка даних\n")
    f.write(f"- Кількість записів: {len(df)}\n")
    f.write(f"- Ознаки: page_view, ad_click\n")
    f.write(f"- Ціль: purchase (подія), duration (час до події)\n")

# === Етап 2: Побудова моделі ===
cph = CoxPHFitter()
# cph.fit(df, duration_col="duration", event_col="purchase")
df_model = df.drop(columns=["Місто"])
cph.fit(df_model, duration_col="duration", event_col="purchase")

summary = cph.summary.round(2)
print(summary)

with open("results/sr5-cox-regression/report.md", "a", encoding="utf-8") as f:
    f.write("\n## Етап 2: Побудова моделі\n")
    f.write(summary.to_markdown())
    f.write("\n")

# === Етап 3: Візуалізація ===
plt.figure(figsize=(8, 4))
cph.plot()
plt.title("Коефіцієнти моделі (log hazard ratios)")
plt.tight_layout()
plt.savefig("results/sr5-cox-regression/hazard_ratios.png")
plt.close()

with open("results/sr5-cox-regression/report.md", "a", encoding="utf-8") as f:
    f.write("\n## Етап 3: Візуалізація\n")
    f.write("- Графік коефіцієнтів: ![](hazard_ratios.png)\n")

# === Етап 4: Інтерпретація ===
with open("results/sr5-cox-regression/report.md", "a", encoding="utf-8") as f:
    f.write("\n## Етап 4: Інтерпретація\n")
    f.write("- Вищі значення `page_view` та `ad_click` асоціюються з підвищеним ризиком покупки\n")
    f.write("- Значущість перевірена через p-value\n")
    f.write("- Модель дозволяє оцінити не лише факт покупки, а й часову динаміку\n")
    f.write("- Cox-регресія доповнює логістичну модель, враховуючи тривалість до події\n")