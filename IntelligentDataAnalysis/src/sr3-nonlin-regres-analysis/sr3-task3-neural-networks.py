import os
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Завантаження даних
df = pd.read_csv("data/sr3-neural-networks.csv")

# Ознаки та ціль
X = df[['page_view', 'ad_click']]
y = df['purchase']

# Побудова нейромережі з 1 прихованим шаром (3–1), логістична активація
model = MLPClassifier(
    hidden_layer_sizes=(3,),
    activation='logistic',
    max_iter=1000,
    random_state=42
)
model.fit(X, y)

# Прогноз і оцінка
y_pred = model.predict(X)
df['actual'] = y
df['predicted'] = y_pred
misclassified = df[df['actual'] != df['predicted']]

# Створення сітки для візуалізації
x_min, x_max = X['page_view'].min() - 1, X['page_view'].max() + 1
y_min, y_max = X['ad_click'].min() - 1, X['ad_click'].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                     np.linspace(y_min, y_max, 300))
grid = np.c_[xx.ravel(), yy.ravel()]
grid_df = pd.DataFrame(grid, columns=X.columns)  # Додаємо назви ознак
Z = model.predict(grid_df).reshape(xx.shape)     # Прогноз без попередження

# Побудова графіка класифікації з помилками
plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, cmap='coolwarm', alpha=0.3)

# Всі точки
colors = ['blue' if label == 0 else 'red' for label in y]
plt.scatter(X['page_view'], X['ad_click'], c=colors, edgecolor='k', s=80, label='Правильно класифіковані')

# Помилки — чорні хрестики
plt.scatter(misclassified['page_view'], misclassified['ad_click'], c='black', marker='x', s=100, label='Помилки')

plt.title("Графік класифікації нейромережі (3–1)")
plt.xlabel("page_view")
plt.ylabel("ad_click")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/sr3-nonlin-regres-analysis/sr3-task3-decision-boundary.png")
plt.close()

# Вивід у консоль
print("Неправильно класифіковані об'єкти:")
print(misclassified)

print("\nМетрики класифікації:")
print(classification_report(y, y_pred, zero_division=0))

print(f"\nТочність: {accuracy_score(y, y_pred):.2f}")

# Створення звіту
with open("results/sr3-nonlin-regres-analysis/report-neural-net.md", "w", encoding="utf-8") as f:
    f.write("# Звіт: Нейронна мережа для прогнозу покупки\n\n")
    f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

    f.write("## Мета\n\n")
    f.write("Синтезувати одношарову нейромережу для класифікації факту покупки на основі поведінкових ознак (`page_view`, `ad_click`).\n\n")

    f.write("## Архітектура\n\n")
    f.write("- Кількість шарів: 2 (1 прихований + 1 вихідний)\n")
    f.write("- Структура: 3–1\n")
    f.write("- Функція активації: логістична сигмоїдна\n\n")

    f.write("## Розрахунки\n\n")
    f.write("```\n")
    f.write(classification_report(y, y_pred, zero_division=0))
    f.write(f"\nТочність: {accuracy_score(y, y_pred):.2f}\n")
    f.write("```\n\n")

    if not misclassified.empty:
        f.write(f"### Неправильно класифіковані об'єкти ({len(misclassified)}):\n\n")
        f.write(misclassified.to_markdown(index=False))
        f.write("\n\n")

    f.write("## Графік класифікації\n\n")
    f.write("На графіку нижче показано, як нейромережа розділяє простір ознак `page_view` та `ad_click`.\n")
    f.write("Червоні точки — клас “купив”, сині — “не купив”.\n")
    f.write("Чорні хрестики — неправильно класифіковані об'єкти.\n\n")
    f.write("![Decision Boundary](sr3-task3-decision-boundary.png)\n\n")

    f.write("## Висновки\n\n")
    f.write(f"Модель досягла точності {accuracy_score(y, y_pred):.2f} та неправильно класифікувала {len(misclassified)} об'єктів.\n")
    f.write("Це свідчить про наявність граничних випадків, які можуть бути покращені шляхом:\n")
    f.write("- Додавання нових ознак (наприклад, `page_view * ad_click`)\n")
    f.write("- Зміни архітектури (більше нейронів або шарів)\n")
    f.write("- Спробування іншої функції активації (`tanh`, `relu`)\n")

print("\nЗвіт сформовано: report-neural-net.md")