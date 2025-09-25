import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr, shapiro
from datetime import datetime

# df = pd.read_csv("data/sr1-correlation-test-ai.csv")
df = pd.read_csv("data/sr1-analytics-google-flue.csv")
# x = df['X']
# y = df['Y']
# x_name = "X1"
# y_name = "Y1"
x = df['page_view']
y = df['ad_click']
x_name = "Page Views (page_view)"
y_name = "Clicks (ad_click)"

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
sns.histplot(x, kde=True, color='skyblue')
plt.title(f"Гістограма {x_name}")

plt.subplot(1, 2, 2)
sns.histplot(y, kde=True, color='salmon')
plt.title(f"Гістограма {y_name}")
plt.tight_layout()
plt.savefig('results/sr1-correlation/histograms.png')
plt.close()

sns.scatterplot(x=x, y=y, data=df)
plt.title(f"Діаграма розсіювання {x_name} та {y_name}")
plt.savefig('results/sr1-correlation/scatterplot.png')
plt.close()

stat_x, p_x = shapiro(x)
stat_y, p_y = shapiro(y)

print(f"Shapiro-Wilk X: p={p_x:.4f}, Y: p={p_y:.4f}")

if p_x > 0.05 and p_y > 0.05:
    method = 'Pearson'
    corr, pval = pearsonr(x, y)
else:
    method = 'Spearman'
    corr, pval = spearmanr(x, y)

print(f"Метод кореляції: {method}")
print(f"Коефіцієнт кореляції: {corr:.4f}")
print(f"p-value: {pval:.4f}")

if abs(corr) < 0.3:
    strength = 'слабкий'
elif abs(corr) < 0.7:
    strength = 'середній'
else:
    strength = 'сильний'

direction = 'прямий' if corr > 0 else 'обернений'

print(f"Тип зв’язку: {direction}, сила: {strength}")

with open("results/sr1-correlation/report.md", "a", encoding="utf-8") as f:
    f.write(f"\n## Результати для {x_name} vs {y_name}\n")
    f.write(f"- Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"- Метод кореляції: {method}\n")
    f.write(f"- Коефіцієнт: {corr:.4f}\n")
    f.write(f"- p-value: {pval:.4f}\n")
    f.write(f"- Тип зв’язку: {direction}, сила: {strength}\n")
    f.write(f"- Гістограми: ![Розподіл значень](histograms.png)\n")
    f.write(f"- Scatterplot: ![Графік кореляції](scatterplot.png)\n")