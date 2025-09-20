import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, accuracy_score
from datetime import datetime

# Завантаження даних
df = pd.read_csv("data/sr3-decision-tree.csv")

# Ознаки та ціль
X = df[['page_view', 'ad_click']]
y = df['purchase']

# Побудова моделі
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X, y)

# Візуалізація дерева
os.makedirs("results/sr3-nonlin-regres-analysis", exist_ok=True)
# plt.figure(figsize=(10, 6))
plt.figure(figsize=(14, 10))
# plot_tree(model, feature_names=X.columns, class_names=["No", "Yes"], filled=True)
plot_tree(
    model,
    feature_names=X.columns,
    class_names=["No", "Yes"],
    filled=True,
    rounded=True,              # Закруглені вузли
    proportion=False,          # Вузли однакового розміру
    precision=2,               # Кількість знаків після коми
    fontsize=12                # Збільшити шрифт
)
plt.title("Дерево рішень для прогнозу покупки")
plt.savefig("results/sr3-nonlin-regres-analysis/sr3-task2-decision-tree.png")
plt.close()

# Прогноз і оцінка
y_pred = model.predict(X)

# Порівняння реальних і передбачених значень
df['actual'] = y
df['predicted'] = y_pred

# Вивести неправильно класифіковані об'єкти
misclassified = df[df['actual'] != df['predicted']]
print("Неправильно класифіковані об'єкти:")
print(misclassified)

# Вивести відомості про модель
print(classification_report(y, y_pred))
print(f"Точність: {accuracy_score(y, y_pred):.2f}")

# Збереження звіту
with open("results/sr3-nonlin-regres-analysis/report-decision-tree.md", "w", encoding="utf-8") as f:
    f.write("# Звіт: Побудова дерева рішень для прогнозу покупки\n\n")
    f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("## Мета\n\n")
    f.write("Синтезувати модель дерева рішень для класифікації факту покупки на основі поведінкових ознак користувача (`page_view`, `ad_click`).\n\n")

    f.write("## Візуалізація\n\n")
    f.write("![](results/sr3-nonlin-regres-analysis/sr3-task2-decision-tree.png)\n\n")

    f.write("## Розрахунки\n\n")
    f.write("```\n")
    f.write(classification_report(y, y_pred))
    f.write(f"\nТочність: {accuracy_score(y, y_pred):.2f}\n")
    f.write("```\n\n")

    if not misclassified.empty:
        f.write("### Неправильно класифіковані об'єкти\n\n")
        f.write(misclassified.to_markdown(index=False))
        f.write("\n\n")

    f.write("## Висновки\n\n")
    f.write("Модель досягла високої точності (95%) та дозволяє інтерпретувати логіку прийняття рішень. Виявлено граничний випадок (Дніпро), який може бути покращений шляхом додавання нових ознак або поглибленням дерева.\n")