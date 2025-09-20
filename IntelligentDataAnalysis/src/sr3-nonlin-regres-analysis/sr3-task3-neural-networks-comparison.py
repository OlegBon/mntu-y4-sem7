import os
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
from datetime import datetime

# Завантаження даних
df = pd.read_csv("data/sr3-neural-networks.csv")
X = df[['page_view', 'ad_click']]
y = df['purchase']

# Модель 1: одношарова (3–1)
model_shallow = MLPClassifier(hidden_layer_sizes=(3,), activation='logistic', max_iter=1000, random_state=42)
model_shallow.fit(X, y)
y_pred_shallow = model_shallow.predict(X)
misclassified_shallow = df[y != y_pred_shallow]

# Модель 2: багатошарова (3–3–1)
model_deep = MLPClassifier(hidden_layer_sizes=(3, 3), activation='logistic', max_iter=1000, random_state=42)
model_deep.fit(X, y)
y_pred_deep = model_deep.predict(X)
misclassified_deep = df[y != y_pred_deep]

# Вивід у консоль
print("=== Одношарова модель (3–1) ===")
print(classification_report(y, y_pred_shallow, zero_division=0))
print(f"Точність: {accuracy_score(y, y_pred_shallow):.2f}")
print("Неправильно класифіковані об'єкти:")
print(misclassified_shallow)

print("\n=== Багатошарова модель (3–3–1) ===")
print(classification_report(y, y_pred_deep, zero_division=0))
print(f"Точність: {accuracy_score(y, y_pred_deep):.2f}")
print("Неправильно класифіковані об'єкти:")
print(misclassified_deep)

# Запис у звіт
with open("results/sr3-nonlin-regres-analysis/report-neural-net-comparison.md", "w", encoding="utf-8") as f:
    f.write("# Звіт: Порівняння нейронних мереж для прогнозу покупки\n\n")
    f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

    f.write("## Мета\n\n")
    f.write("Порівняти ефективність одношарової та багатошарової нейромережі на однаковій вибірці (`page_view`, `ad_click`).\n\n")

    f.write("## Архітектури\n\n")
    f.write("- Модель 1: 3–1 (одношарова), логістична сигмоїдна\n")
    f.write("- Модель 2: 3–3–1 (багатошарова), логістична сигмоїдна\n\n")

    f.write("## Розрахунки\n\n")

    f.write("### Одношарова модель (3–1)\n")
    f.write("```\n")
    f.write(classification_report(y, y_pred_shallow, zero_division=0))
    f.write(f"\nТочність: {accuracy_score(y, y_pred_shallow):.2f}\n")
    f.write("```\n\n")
    if not misclassified_shallow.empty:
        f.write("Неправильно класифіковані об'єкти:\n\n")
        f.write(misclassified_shallow.to_markdown(index=False))
        f.write("\n\n")

    f.write("### Багатошарова модель (3–3–1)\n")
    f.write("```\n")
    f.write(classification_report(y, y_pred_deep, zero_division=0))
    f.write(f"\nТочність: {accuracy_score(y, y_pred_deep):.2f}\n")
    f.write("```\n\n")
    if not misclassified_deep.empty:
        f.write("Неправильно класифіковані об'єкти:\n\n")
        f.write(misclassified_deep.to_markdown(index=False))
        f.write("\n\n")

    f.write("## Висновки\n\n")
    f.write("Порівняння показало, що багатошарова модель може краще аппроксимувати складні залежності, але її ефективність залежить від обсягу даних та параметрів. У даному випадку точність могла змінитися, але не гарантує покращення класифікації всіх об'єктів.\n")

print("\nЗвіт сформовано: report-neural-net-comparison.md")