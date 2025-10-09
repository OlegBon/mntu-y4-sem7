import pandas as pd
import numpy as np
import os

# Список завдань
tasks = [
    {'name': 'task0', 'filename': 'pr3_task0_data.csv'},
    {'name': 'task1', 'filename': 'pr3_task1_data.csv'},
    {'name': 'task2', 'filename': 'pr3_task2_data.csv'},
    {'name': 'task3', 'filename': 'pr3_task3_data.csv'},
    {'name': 'task4', 'filename': 'pr3_task4_data.csv'},
    {'name': 'task5', 'filename': 'pr3_task5_data.csv'},
]

for task in tasks:
    print(f"\n🔄 Обробка завдання pr3_{task['name']}")

    # Шляхи до файлів
    data_path = os.path.join('data', task['filename'])
    result_path = os.path.join('results', f"pr3_{task['name']}_discriminant_analysis.md")

    # Завантаження даних
    df = pd.read_csv(data_path)

    # Розділення на класи
    class_A = df[df['Class'] == 'A'][['X1', 'X2', 'X3']].values
    class_B = df[df['Class'] == 'B'][['X1', 'X2', 'X3']].values
    Z = df[df['Class'].str.startswith('Z')][['ID', 'X1', 'X2', 'X3']]

    # Середні значення
    mean_A = np.mean(class_A, axis=0)
    mean_B = np.mean(class_B, axis=0)

    # Коваріаційні матриці (зміщені, як у методичці)
    cov_A = np.round(np.cov(class_A, rowvar=False, bias=True), 5)
    cov_B = np.round(np.cov(class_B, rowvar=False, bias=True), 5)

    # Пулінгова матриця (незміщена оцінка сумарної коваріаційної матриці)
    n1, n2 = len(class_A), len(class_B)
    pooled_cov = (n1 * cov_A + n2 * cov_B) / (n1 + n2 - 2)

    # Зворотна матриця
    inv_cov = np.linalg.inv(pooled_cov)

    # Вектор коефіцієнтів дискримінації
    a = inv_cov @ (mean_A - mean_B)

    # Дискримінантні оцінки для навчальних об'єктів
    scores_A = [x @ a for x in class_A]
    scores_B = [x @ a for x in class_B]

    # Центри класів
    Ux = mean_A @ a
    Uy = mean_B @ a
    C = (Ux + Uy) / 2

    # Класифікація Z1, Z2, ...
    results = []
    for _, row in Z.iterrows():
        features = np.array([row['X1'], row['X2'], row['X3']])
        score = features @ a
        predicted_class = 'A' if score > C else 'B'
        results.append({
            'ID': int(row['ID']),
            'Score': round(score, 4),
            'Threshold': round(C, 4),
            'Predicted_Class': predicted_class
        })

    # Критерій λ Уїлкса
    global_mean = (n1 * mean_A + n2 * mean_B) / (n1 + n2)

    Qsw = np.sum((class_A - mean_A)**2) + np.sum((class_B - mean_B)**2)
    Qsb = n1 * np.sum((mean_A - global_mean)**2) + n2 * np.sum((mean_B - global_mean)**2)

    wilks_lambda = Qsb / Qsw
    Lw = 1 / (1 + wilks_lambda)

    # Вплив ознак
    abs_a = np.abs(a)
    R = abs_a / np.sum(abs_a)
    R_percent = np.round(R * 100, 2)

    # Формування звіту
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(f"# Практична 3 — Дискримінантний аналіз ({task['name']})\n\n")
        f.write(f"## 1. Середні значення ознак\n\n")
        f.write(f"| Ознака | Клас A (X̄) | Клас B (Ȳ) |\n|--------|-------------|-------------|\n")
        for i, label in enumerate(['X1', 'X2', 'X3']):
            f.write(f"| {label} | {mean_A[i]:.2f} | {mean_B[i]:.2f} |\n")

        f.write(f"\n## 2. Коваріаційні матриці\n\n**Sx:**\n```\n{cov_A}\n```\n**Sy:**\n```\n{cov_B}\n```\n")
        f.write(f"\n## 3. Пулінгова матриця (незміщена оцінка сумарної коваріаційної матриці)\n```\n{np.round(pooled_cov, 5)}\n```\n")
        f.write(f"\n## 4. Зворотна матриця\n```\n{np.round(inv_cov, 4)}\n```\n")
        f.write(f"\n## 5. Вектор коефіцієнтів дискримінації\n```\n{np.round(a, 4)}\n```\n")

        f.write(f"\n## 6. Оцінки дискримінантних функцій для навчальних об'єктів\n\n")
        f.write(f"| ID | Клас | Оцінка U |\n|----|------|-----------|\n")
        for i, score in enumerate(scores_A):
            f.write(f"| {i+1} | A | {score:.4f} |\n")
        for i, score in enumerate(scores_B):
            f.write(f"| {i+5} | B | {score:.4f} |\n")

        f.write(f"\n**Ux = {Ux:.4f}**, **Uy = {Uy:.4f}**, **C = {C:.4f}**\n")

        f.write(f"\n## 7. Класифікація об'єктів для розпізнавання\n\n")
        f.write(f"| ID | X1 | X2 | X3 | Uz | Клас |\n|----|----|----|----|------|------|\n")
        for row in results:
            z_row = Z[Z['ID'] == row['ID']].iloc[0]
            f.write(f"| {row['ID']} | {z_row['X1']} | {z_row['X2']} | {z_row['X3']} | {row['Score']} | {row['Predicted_Class']} |\n")

        f.write(f"\n## 8. Критерій λ Уїлкса\n\n")
        f.write(f"- Внутрішньогрупова варіація (Qsw): {Qsw:.4f}\n")
        f.write(f"- Міжгрупова варіація (Qsb): {Qsb:.4f}\n")
        f.write(f"- λ Уїлкса: {wilks_lambda:.4f}\n")
        f.write(f"- Lw: {Lw:.4f}\n")
        f.write(f"\n## 9. Вплив ознак на дискримінацію\n\n")
        f.write(f"| Ознака | Вплив (%) |\n|--------|------------|\n")
        for i, label in enumerate(['X1', 'X2', 'X3']):
            f.write(f"| {label} | {R_percent[i]:.2f} |\n")

        f.write(f"\n**Найбільший внесок:** {['X1','X2','X3'][np.argmax(R_percent)]} — {np.max(R_percent):.2f}%\n")

    print(f"✅ Звіт збережено у: {result_path}")