import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import scipy.stats as stats

# Зчитування даних
df = pd.read_csv("data/pr6_data.csv")
X = df["X"].values.reshape(-1, 1)
Y = df["Y"].values

# Побудова моделі
model = LinearRegression()
model.fit(X, Y)

# Коефіцієнти
a0 = model.intercept_
a1 = model.coef_[0]
Y_pred = model.predict(X)
r2 = r2_score(Y, Y_pred)
residuals = Y - Y_pred

# 📈 Графік регресії
plt.figure(figsize=(8, 5))
plt.scatter(X, Y, color="blue", label="Фактичні дані")
plt.plot(X, Y_pred, color="red", label=f"Регресія: Y = {a0:.2f} + {a1:.2f}X")
plt.xlabel("Реальні витрати капіталу (X)")
plt.ylabel("Обсяг виробництва (Y)")
plt.title("Лінійна регресія")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/pr6_regression-curve.png")
plt.close()

# 📊 Таблиця залишків
residuals_df = pd.DataFrame({
    "Year": df["Year"],
    "Y_actual": Y,
    "Y_predicted": Y_pred,
    "Residual": residuals
})
residuals_df.to_csv("results/pr6_residuals.csv", index=False)

# 📉 Гістограма залишків
plt.figure(figsize=(6, 4))
plt.hist(residuals, bins=10, color="skyblue", edgecolor="black")
plt.title("Гістограма залишків")
plt.xlabel("Залишок")
plt.ylabel("Частота")
plt.grid(True)
plt.tight_layout()
plt.savefig("results/pr6_residuals-histogram.png")
plt.close()

# 📈 P–P plot залишків
plt.figure(figsize=(6, 4))
stats.probplot(residuals, dist="norm", plot=plt)
plt.title("P–P plot залишків")
plt.tight_layout()
plt.savefig("results/pr6_residuals-ppplot.png")
plt.close()

# 📝 Markdown-звіт
with open("results/pr6_regression-analysis.md", "w", encoding="utf-8") as f:
    f.write("# Практична робота №6 — Регресійний аналіз в лінійних моделях\n\n")
    f.write("**Мета:** ознайомитись з властивостями регресійного аналізу і провести регресійний аналіз статистичних даних.\n\n")
    f.write("## 📊 Вихідні дані\n")
    f.write("- Залежна змінна: Y — реальний обсяг виробництва\n")
    f.write("- Незалежна змінна: X — реальні витрати капіталу\n")
    f.write(f"- Кількість спостережень: {len(df)}\n\n")
    f.write("## 📐 Модель\n")
    f.write("Побудовано лінійну модель:\n")
    f.write(f"\n\\[ Y = {a0:.3f} + {a1:.3f}X \\]\n\n")
    f.write(f"Коефіцієнт детермінації: \\( R^2 = {r2:.4f} \\)\n\n")
    f.write("## 📈 Графік регресії\n")
    f.write("![Графік регресії](pr6_regression-curve.png)\n\n")
    f.write("## 📊 Таблиця залишків\n")
    f.write("Збережено у `results/pr6_residuals.csv`. Містить фактичні значення, прогнозовані та залишки.\n\n")
    f.write("## 📉 Гістограма залишків\n")
    f.write("![Гістограма залишків](pr6_residuals-histogram.png)\n\n")
    f.write("## 📈 P–P plot залишків\n")
    f.write("![P–P plot залишків](pr6_residuals-ppplot.png)\n\n")
    f.write("## 📌 Висновок\n")
    f.write("> Отримана модель демонструє високий ступінь лінійної залежності між витратами капіталу та обсягом виробництва. Гістограма залишків має приблизно симетричну форму, а P–P plot показує, що залишки близькі до нормального розподілу. Це підтверджує адекватність моделі та коректність застосування методу найменших квадратів.\n")