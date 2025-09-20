import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import statsmodels.api as sm

# Шляхи
DATA_PATH = 'data/sr4-logistic-regression.csv'
RESULTS_DIR = 'results/sr4-logistic-regression'
REPORT_PATH = os.path.join(RESULTS_DIR, 'report.md')
PLOT_BOUNDARY_PATH = os.path.join(RESULTS_DIR, 'decision_boundary.png')
PLOT_PAGEVIEW_PATH = os.path.join(RESULTS_DIR, 'logistic_curve_page_view.png')
PLOT_ADCLICK_PATH = os.path.join(RESULTS_DIR, 'logistic_curve_ad_click.png')

# Створення папки результатів
os.makedirs(RESULTS_DIR, exist_ok=True)

# Завантаження даних
df = pd.read_csv(DATA_PATH)
X = df[['page_view', 'ad_click']]
y = df['purchase']

# Побудова моделі
model = LogisticRegression()
model.fit(X, y)

# Прогноз
y_pred = model.predict(X)
y_prob = model.predict_proba(X)[:, 1]
df['actual'] = y
df['predicted'] = y_pred
misclassified = df[df['actual'] != df['predicted']]

# Метрики
acc = accuracy_score(y, y_pred)
report = classification_report(y, y_pred, digits=2)
conf_matrix = confusion_matrix(y, y_pred)

# Вивід у консоль
print("=== Logistic Regression Report ===")
print(f"Accuracy: {acc:.2f}")
print("\nClassification Report:")
print(report)
print("\nConfusion Matrix:")
print(conf_matrix)

if not misclassified.empty:
    print("\nНеправильно класифіковані об'єкти:")
    print(misclassified[['Місто', 'page_view', 'ad_click', 'purchase', 'actual', 'predicted']].to_string(index=True))
else:
    print("\nУсі об'єкти класифіковано правильно.")

# Запис у Markdown-звіт
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write("# Звіт: Логістична регресія\n\n")
    f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write(f"**Точність (accuracy):** {acc:.2f}\n\n")
    f.write("## Класифікаційний звіт\n")
    f.write("```\n" + report + "\n```\n")
    f.write("## Матриця помилок\n")
    f.write("```\n" + str(conf_matrix) + "\n```\n")

# Візуалізація межі класифікації
def plot_decision_boundary(X, y, model):
    h = 0.5
    x_min, x_max = X['page_view'].min() - 1, X['page_view'].max() + 1
    y_min, y_max = X['ad_click'].min() - 1, X['ad_click'].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    grid = pd.DataFrame({'page_view': xx.ravel(), 'ad_click': yy.ravel()})
    probs = model.predict(grid).reshape(xx.shape)

    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, probs, cmap='coolwarm', alpha=0.3)

    # Об'єднуємо X і y для коректного hue
    df_plot = X.copy()
    df_plot['purchase'] = y

    sns.scatterplot(
        x='page_view',
        y='ad_click',
        hue='purchase',
        palette={0: 'blue', 1: 'red'},
        data=df_plot,
        legend=False
    )

    plt.title('Межа класифікації логістичної регресії')
    plt.xlabel('page_view')
    plt.ylabel('ad_click')
    plt.tight_layout()
    plt.savefig(PLOT_BOUNDARY_PATH)
    plt.close()

plot_decision_boundary(X, y, model)

# Побудова логістичної кривої з довірчим інтервалом
def plot_logistic_curve(X, y, feature, save_path):
    X_sm = sm.add_constant(X[feature])
    model_sm = sm.Logit(y, X_sm).fit(disp=False)

    x_vals = np.linspace(X[feature].min(), X[feature].max(), 100)
    x_vals_sm = sm.add_constant(x_vals)
    preds = model_sm.predict(x_vals_sm)

    pred_summary = model_sm.get_prediction(x_vals_sm).summary_frame(alpha=0.05)
    lower = pred_summary['ci_lower']
    upper = pred_summary['ci_upper']

    # Об'єднуємо X і y для коректного hue
    df_plot = X.copy()
    df_plot['purchase'] = y

    plt.figure(figsize=(8, 6))

    # Всі точки
    colors = ['blue' if label == 0 else 'red' for label in y]
    plt.scatter(X['page_view'], X['ad_click'], c=colors, edgecolor='k', s=80, label='Правильно класифіковані')

    # Помилки — чорні хрестики
    plt.scatter(misclassified['page_view'], misclassified['ad_click'], c='black', marker='x', s=100, label='Помилки')

    plt.title("Графік класифікації логістичної регресії з помилками")
    plt.xlabel("page_view")
    plt.ylabel("ad_click")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/sr4-logistic-regression/decision_boundary_errors.png")
    plt.close()

# Побудова кривих для обох ознак
plot_logistic_curve(X, y, 'page_view', PLOT_PAGEVIEW_PATH)
plot_logistic_curve(X, y, 'ad_click', PLOT_ADCLICK_PATH)

# Додавання опису до звіту
with open(REPORT_PATH, 'a', encoding='utf-8') as f:
    if not misclassified.empty:
        f.write(f"\n## Неправильно класифіковані об'єкти ({len(misclassified)}):\n\n")
        f.write("У таблиці нижче наведено об'єкти, які модель класифікувала неправильно:\n\n")
        f.write(misclassified.to_markdown(index=False))
        f.write("\n\n")

    f.write("## Графік класифікації з помилками\n")
    f.write("На графіку нижче показано, як модель логістичної регресії розділяє простір ознак `page_view` та `ad_click`.\n")
    f.write("Червоні точки — клас “купив”, сині — “не купив”.\n")
    f.write("Чорні хрестики — неправильно класифіковані об'єкти.\n\n")
    f.write("![Межа класифікації з помилками](decision_boundary_errors.png)\n\n")

    f.write("\n## Межа класифікації логістичної регресії\n")
    f.write("На графіку показано, як модель логістичної регресії розділяє простір ознак `page_view` та `ad_click`.\n")
    f.write("Фон зафарбований відповідно до передбаченого класу: червоний — не купив, синій — купив.\n")
    f.write("Точки — реальні об'єкти, кольором позначено фактичний клас.\n")
    f.write("![Межа класифікації](decision_boundary.png)\n")

    f.write("\n## Логістична крива для ознаки `page_view`\n")
    f.write("На графіку показано, як змінюється ймовірність покупки залежно від кількості переглядів сторінок.\n")
    f.write("Чорна крива — модель логістичної регресії, сірий фон — 95% довірчий інтервал.\n")
    f.write("![Логістична крива page_view](logistic_curve_page_view.png)\n")

    f.write("\n## Логістична крива для ознаки `ad_click`\n")
    f.write("На графіку показано, як змінюється ймовірність покупки залежно від кількості кліків по рекламі.\n")
    f.write("Чорна крива — модель логістичної регресії, сірий фон — 95% довірчий інтервал.\n")
    f.write("![Логістична крива ad_click](logistic_curve_ad_click.png)\n")