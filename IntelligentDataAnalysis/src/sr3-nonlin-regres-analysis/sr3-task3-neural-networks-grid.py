import os
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
from datetime import datetime

# Завантаження даних
df = pd.read_csv("data/sr3-neural-networks.csv")
X = df[['page_view', 'ad_click']]
y = df['purchase']

# Конфігурації моделей
configs = [
    ("shallow", (3,), "logistic"),
    ("deep", (3, 3), "logistic"),
    ("wider", (6, 6), "logistic"),
    ("deeper", (6, 6, 6), "logistic"),
    ("tanh_deep", (6, 6, 6), "tanh"),
]

results = []

# Побудова моделей
for name, layers, activation in configs:
    model = MLPClassifier(hidden_layer_sizes=layers, activation=activation, max_iter=2000, random_state=42)
    model.fit(X, y)
    y_pred = model.predict(X)
    acc = accuracy_score(y, y_pred)
    report = classification_report(y, y_pred, zero_division=0)
    misclassified = df[y != y_pred]
    results.append((name, layers, activation, acc, report, misclassified))

# Вивід у консоль
for name, layers, activation, acc, report, misclassified in results:
    print(f"\n=== Модель: {name} ===")
    print(f"Архітектура: {layers}, Активація: {activation}")
    print(f"Точність: {acc:.2f}")
    print("Класифікація:")
    print(report)
    print("Неправильно класифіковані об'єкти:")
    print(misclassified)

# Запис у звіт
with open("results/sr3-nonlin-regres-analysis/report-neural-net-grid.md", "w", encoding="utf-8") as f:
    f.write("# Звіт: Порівняння архітектур нейронних мереж\n\n")
    f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("## Мета\n\n")
    f.write("Провести експеримент з різними архітектурами нейромереж для класифікації факту покупки на основі ознак `page_view` та `ad_click`.\n\n")

    for name, layers, activation, acc, report, misclassified in results:
        f.write(f"### Модель: {name}\n")
        f.write(f"- Архітектура: {layers}\n")
        f.write(f"- Активація: {activation}\n")
        f.write(f"- Точність: {acc:.2f}\n\n")
        f.write("```\n")
        f.write(report)
        f.write("```\n\n")
        if not misclassified.empty:
            f.write("Неправильно класифіковані об'єкти:\n\n")
            f.write(misclassified.to_markdown(index=False))
            f.write("\n\n")

    f.write("## Висновки\n\n")
    f.write("Більш глибокі та широкі архітектури можуть покращити точність, але не гарантують ідеальну класифікацію. Найкращі результати досягаються при балансі між складністю моделі та обсягом даних. Рекомендується додати нові ознаки або збільшити вибірку для подальшого покращення.\n")

print("\nЗвіт сформовано: report-neural-net-grid.md")