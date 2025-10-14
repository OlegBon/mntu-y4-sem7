import pandas as pd
import numpy as np
import os
import math

tasks = [
    {'name': 'task0', 'filename': 'pr4_task0_data.csv'},
    {'name': 'task1', 'filename': 'pr4_task1_data.csv'},
]

os.makedirs('results', exist_ok=True)

for task in tasks:
    print(f"\n🔄 Обробка завдання pr4_{task['name']}")

    data_path = os.path.join('data', task['filename'])
    result_path = os.path.join('results', f"pr4_{task['name']}_analysis-of-variance.md")

    df = pd.read_csv(data_path)

    # 1. Середні значення
    df["Sum"] = df.iloc[:, 1:5].sum(axis=1)
    df["Mean"] = df.iloc[:, 1:5].mean(axis=1)
    rep_sums = df.iloc[:, 1:5].sum(axis=0)
    rep_means = df.iloc[:, 1:5].mean(axis=0)
    grand_total = df["Sum"].sum()
    grand_mean = df["Mean"].mean()

    # Округлення для виводу
    df_display = df.copy()
    df_display["Sum"] = df_display["Sum"].round(1)
    df_display["Mean"] = df_display["Mean"].round(1)
    rep_sums_display = rep_sums.round(1)

    rep_cols = df.columns[1:5]
    X = df.loc[:, rep_cols].astype(float)

    # 2. Перетворення: X = X − A
    A = grand_mean.round(0)
    transformed = df.loc[:, rep_cols] - A
    transformed["Σ'"] = transformed.sum(axis=1)

    rep_sums_transformed = transformed.loc[:, rep_cols].sum(axis=0)
    total_row_sum = transformed["Σ'"].sum()
    transformed.loc["∑P"] = list(rep_sums_transformed) + [total_row_sum]

    transformed_display = transformed.round(1)

    # 3. Квадрати перетворених значень
    squared = transformed.loc[:, rep_cols] ** 2
    squared["Σ²"] = transformed.loc[:, rep_cols].sum(axis=1) ** 2

    rep_sums_for_P2 = transformed.loc["∑P", rep_cols].astype(float)
    rep_squares_for_P2 = rep_sums_for_P2 ** 2
    sum_of_squares_cols = rep_squares_for_P2.sum()

    sum_squared_P2_for_C = float(squared.loc["∑P", "Σ²"])

    # 4. Загальна кількість спостережень
    N = df.shape[0] * len(rep_cols)

    # 5. Корегуючий фактор
    C = sum_squared_P2_for_C / N

    # 6. Загальна сума квадратів
    Cy = squared.loc[:df.shape[0]-1, rep_cols].sum().sum() - C

    # 7. Сума квадратів для повторностей
    Cp = rep_squares_for_P2.sum() / len(rep_cols) - C

    # 8. Сума квадратів для варіантів
    Cv = squared["Σ²"].iloc[:df.shape[0]].sum() / len(rep_cols) - C

    # 9. Сума квадратів для похибки
    Cz = Cy - Cp - Cv

    # 10. Степені свободи
    vy = N - 1
    vv = df.shape[0] - 1
    vp = len(rep_cols) - 1
    vz = vv * vp

    # 11–12. Дисперсії
    Sv = Cv / vv
    Sz = Cz / vz

    # 13. Критерій Фішера
    Ff = Sv / Sz
    Ft = 3.86  # табличне значення для df1=3, df2=9

    # 14. Таблиця дисперсійного аналізу
    anova_table = pd.DataFrame({
        "Джерело варіації": ["Загальна", "Повторностей", "Варіантів", "Похибки"],
        "Сума квадратів": [Cy, Cp, Cv, Cz],
        "Степені свободи": [vy, vp, vv, vz],
        "Середній квадрат": ["—", "—", f"{Sv:.2f}", f"{Sz:.2f}"],
        "Fф": ["—", "—", f"{Ff:.2f}", "—"],
        "Fт": ["—", "—", f"{Ft:.2f}", "—"]
    })

    squared_display = squared.round(2)

    # 15. Похибка для досліду
    Sx = math.sqrt(Sz / len(rep_cols))

    # 16. Похибка різниці середніх
    Sd = 1.41 * Sx

    # 17. Найменша істотна різниця: HIP = t05 * Sd
    t05 = 2.26
    HIP = t05 * Sd

    # 18. Висновки: порівняння з контролем (варіант 1)
    control_mean = df_display.loc[0, "Mean"]
    mean_diffs = df_display["Mean"] - control_mean
    hip_comparison = mean_diffs.apply(lambda x: f"{x:.1f} > {HIP:.2f}" if x > HIP else f"{x:.1f} ≤ {HIP:.2f}")
    hip_table = pd.DataFrame({
        "Варіанти": df_display["Variant"],
        "Середня урожайність, ц/га": df_display["Mean"],
        "Відхилення від контролю, ± ц/га": mean_diffs.round(1),
        "Оцінка відносно НІР₀₅": hip_comparison
    })

    # Формування Markdown-звіту
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(f"# 📊 Дисперсійний аналіз — {task['name']}\n\n")

        f.write("## 1. Середні значення по варіантах:\n\n")
        f.write(df_display[["Variant", "Sum", "Mean"]].to_markdown(index=False))
        f.write("\n\n## Сума по повтореннях:\n\n")
        f.write(rep_sums_display.to_frame(name="ΣP").to_markdown())
        f.write(f"\n\n**Загальна сума (ΣX):** {grand_total:.1f}  \n**Загальне середнє:** {grand_mean:.1f}\n\n")

        f.write("## 2. Перетворені значення (X − A):\n\n")
        f.write(transformed_display.to_markdown())

        f.write("\n\n## 3. Квадрати перетворених значень:\n\n")
        f.write(squared_display.to_markdown())

        f.write("\n\n## 4–13. Основні розрахунки:\n\n")
        f.write(f"- N = {N}\n")
        f.write(f"- C = {C:.2f}\n")
        f.write(f"- Cy = {Cy:.2f}\n")
        f.write(f"- Cp = {Cp:.2f}\n")
        f.write(f"- Cv = {Cv:.2f}\n")
        f.write(f"- Cz = {Cz:.2f}\n")
        f.write(f"- vy = {vy}, vv = {vv}, vp = {vp}, vz = {vz}\n")
        f.write(f"- Sv = {Sv:.2f}, Sz = {Sz:.2f}\n")
        f.write(f"- Fф = {Ff:.2f}, Fт = {Ft:.2f}\n")

        f.write("\n\n## 14. Таблиця дисперсійного аналізу:\n\n")
        f.write(anova_table.to_markdown(index=False))

        f.write("\n\n## 15–18. Похибка та висновки:\n\n")
        f.write(f"- Sx = {Sx:.3f}  \n")
        f.write(f"- Sd = 1.41 × Sx = {Sd:.2f}  \n")
        f.write(f"- НІР₀₅ = t₀₅ × Sd = {HIP:.2f} (t₀₅ = 2.26)\n\n")

        f.write("## 18. Висновки результатів досліду:\n\n")
        f.write(hip_table.to_markdown(index=False))

    print(f"✅ Звіт збережено у: {result_path}")