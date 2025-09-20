import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import os
from datetime import datetime

# Завантаження даних
df = pd.read_csv("data/sr3-nonlin-regres-analysis.csv")

X = df['page_view'].values.reshape(-1, 1)
y = df['ad_click'].values

# Створення папки для графіків
os.makedirs("results/sr3-nonlin-regres-analysis", exist_ok=True)

# Список моделей
models = {}

# Поліном 2-го ступеня
poly2 = PolynomialFeatures(degree=2)
X_poly2 = poly2.fit_transform(X)
model_poly2 = LinearRegression().fit(X_poly2, y)
y_pred_poly2 = model_poly2.predict(X_poly2)
models['Поліном 2-го ступеня'] = (y_pred_poly2, r2_score(y, y_pred_poly2))

# Поліном 3-го ступеня
poly3 = PolynomialFeatures(degree=3)
X_poly3 = poly3.fit_transform(X)
model_poly3 = LinearRegression().fit(X_poly3, y)
y_pred_poly3 = model_poly3.predict(X_poly3)
models['Поліном 3-го ступеня'] = (y_pred_poly3, r2_score(y, y_pred_poly3))

# Гіперболічна модель: Y = a + b / X
X_inv = (1 / df['page_view']).values.reshape(-1, 1)
model_hyper = LinearRegression().fit(X_inv, y)
y_pred_hyper = model_hyper.predict(X_inv)
models['Гіперболічна модель'] = (y_pred_hyper, r2_score(y, y_pred_hyper))

# Степенева модель: Y = a * X^b → логарифмічна трансформація
df_power = df[(df['page_view'] > 0) & (df['ad_click'] > 0)].copy()
X_log = np.log(df_power['page_view']).values.reshape(-1, 1)
y_log = np.log(df_power['ad_click']).values
model_power = LinearRegression().fit(X_log, y_log)
y_pred_power = np.exp(model_power.predict(X_log))
models['Степенева модель'] = (y_pred_power, r2_score(df_power['ad_click'], y_pred_power))

# Експоненціальна модель: Y = a * e^(bX) → логарифмічна трансформація
df_exp = df[df['ad_click'] > 0].copy()
X_exp = df_exp['page_view'].values.reshape(-1, 1)
y_log_exp = np.log(df_exp['ad_click']).values
model_exp = LinearRegression().fit(X_exp, y_log_exp)
y_pred_exp = np.exp(model_exp.predict(X_exp))
models['Експоненціальна модель'] = (y_pred_exp, r2_score(df_exp['ad_click'], y_pred_exp))

# Побудова графіків
plt.figure(figsize=(10, 6))
plt.scatter(df['page_view'], df['ad_click'], color='black', label='Фактичні дані')

x_vals = np.linspace(df['page_view'].min(), df['page_view'].max(), 100).reshape(-1, 1)

# Поліном 2
plt.plot(x_vals, model_poly2.predict(poly2.transform(x_vals)), label='Поліном 2-го ступеня')

# Поліном 3
plt.plot(x_vals, model_poly3.predict(poly3.transform(x_vals)), label='Поліном 3-го ступеня')

# Гіперболічна
plt.plot(x_vals, model_hyper.predict(1 / x_vals), label='Гіперболічна модель')

# Степенева
x_vals_power = np.log(x_vals[x_vals > 0]).reshape(-1, 1)
plt.plot(x_vals[x_vals > 0], np.exp(model_power.predict(x_vals_power)), label='Степенева модель')

# Експоненціальна
plt.plot(x_vals, np.exp(model_exp.predict(x_vals)), label='Експоненціальна модель')

plt.xlabel("page_view")
plt.ylabel("ad_click")
plt.title("Нелінійні регресійні моделі")
# plt.legend()
plt.legend(loc="lower right")
plt.grid(True)
plt.tight_layout()
plt.savefig("results/sr3-nonlin-regres-analysis/nonlinear_models.png")
plt.close()

# # Вивід R²
# print("=== Нелінійний регресійний аналіз. Оцінка якості моделей (R²) ===")
# for name, (y_pred, r2) in models.items():
#     print(f"{name}: R² = {r2:.3f}")

print("\n=== Нелінійний регресійний аналіз. Порівняння моделей ===")
print(f"{'Модель':<25} {'Формула':<50} {'R²':>5}")
print("-" * 85)

# Поліном 2-го ступеня
a2, b2, c2 = model_poly2.coef_[2], model_poly2.coef_[1], model_poly2.intercept_
r2_2 = models['Поліном 2-го ступеня'][1]
formula2 = f"Y={a2:.2f}X² + {b2:.2f}X + {c2:.2f}"
print(f"{'Поліном 2-го ступеня':<25} {formula2:<50} {r2_2:.2f}")

# Поліном 3-го ступеня
a3, b3, c3, d3 = model_poly3.coef_[3], model_poly3.coef_[2], model_poly3.coef_[1], model_poly3.intercept_
r2_3 = models['Поліном 3-го ступеня'][1]
formula3 = f"Y={a3:.2f}X³ + {b3:.2f}X² + {c3:.2f}X + {d3:.2f}"
print(f"{'Поліном 3-го ступеня':<25} {formula3:<50} {r2_3:.2f}")

# Гіперболічна модель
b_h, a_h = model_hyper.coef_[0], model_hyper.intercept_
r2_h = models['Гіперболічна модель'][1]
formula_h = f"Y={a_h:.2f} + {b_h:.2f}/X"
print(f"{'Гіперболічна модель':<25} {formula_h:<50} {r2_h:.2f}")

# Степенева модель
b_p, log_a_p = model_power.coef_[0], model_power.intercept_
a_p = np.exp(log_a_p)
r2_p = models['Степенева модель'][1]
formula_p = f"Y={a_p:.2f} * X^{b_p:.2f}"
print(f"{'Степенева модель':<25} {formula_p:<50} {r2_p:.2f}")

# Експоненціальна модель
b_e, log_a_e = model_exp.coef_[0], model_exp.intercept_
a_e = np.exp(log_a_e)
r2_e = models['Експоненціальна модель'][1]
formula_e = f"Y={a_e:.2f} * e^({b_e:.2f}X)"
print(f"{'Експоненціальна модель':<25} {formula_e:<50} {r2_e:.2f}")

with open("results/sr3-nonlin-regres-analysis/report-nonlin-regres-analysis.md", "w", encoding="utf-8") as f:
    f.write("# Звіт: Нелінійний регресійний аналіз\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("**Мета:** Дослідити форму зв’язку між кількістю переглядів сторінки (`page_view`) та кількістю кліків по рекламі (`ad_click`) за допомогою різних нелінійних регресійних моделей.\n\n")

    f.write("## Вхідні дані\n\n")
    f.write("Вибірка містить 20 міст України з такими ознаками:\n\n")
    f.write("- `page_view` — кількість переглядів сторінки\n")
    f.write("- `ad_click` — кількість кліків по рекламі\n\n")

    f.write("## Побудовані моделі\n\n")
    f.write("| Модель | Формула регресії | R² |\n")
    f.write("|--------|------------------|----|\n")

    # Поліном 2
    formula2 = f"Y={a2:.2f}X² + {b2:.2f}X + {c2:.2f}"
    f.write(f"| Поліном 2-го ступеня | `{formula2}` | {r2_2:.2f} |\n")

    # Поліном 3
    formula3 = f"Y={a3:.2f}X³ + {b3:.2f}X² + {c3:.2f}X + {d3:.2f}"
    f.write(f"| Поліном 3-го ступеня | `{formula3}` | {r2_3:.2f} |\n")

    # Гіперболічна
    formula_h = f"Y={a_h:.2f} + {b_h:.2f}/X"
    f.write(f"| Гіперболічна модель | `{formula_h}` | {r2_h:.2f} |\n")

    # Степенева
    formula_p = f"Y={a_p:.2f} * X^{b_p:.2f}"
    f.write(f"| Степенева модель | `{formula_p}` | {r2_p:.2f} |\n")

    # Експоненціальна
    formula_e = f"Y={a_e:.2f} * e^({b_e:.2f}X)"
    f.write(f"| Експоненціальна модель | `{formula_e}` | {r2_e:.2f} |\n")

    f.write("\n## Візуалізація\n\n")
    f.write("На графіку нижче показано фактичні дані (чорні точки) та криві всіх моделей:\n\n")
    f.write("![Нелінійні регресійні моделі](nonlinear_models.png)\n\n")

    f.write("## Висновки\n\n")
    f.write("- Найкраще апроксимує залежність **поліном 3-го ступеня** (R² = {:.2f})\n".format(r2_3))
    f.write("- **Степенева модель** також показала високу якість (R² = {:.2f}) і є простішою для інтерпретації\n".format(r2_p))
    f.write("- **Гіперболічна та експоненціальна моделі** мають нижчі R², але можуть бути корисні для опису граничних випадків\n")
    f.write("- Всі моделі демонструють **нелінійний характер зв’язку** між `page_view` та `ad_click`\n\n")

    f.write("## Рекомендації\n\n")
    f.write("- Для подальшого аналізу варто протестувати моделі на нових даних або додати додаткові ознаки (наприклад, взаємодію `page_view * ad_click`)\n")
    f.write("- Можна порівняти ці результати з класифікаційними моделями з Практичної 1\n\n")
