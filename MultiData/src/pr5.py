import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

tasks = [
    {'name': 'task1', 'filename': 'pr5_task1_data.csv'},
    {'name': 'task2', 'filename': 'pr5_task2_data.csv'},
    {'name': 'task3', 'filename': 'pr5_task3_data.csv'},
    {'name': 'task4', 'filename': 'pr5_task4_data.csv'},
    {'name': 'task5', 'filename': 'pr5_task5_data.csv'},
]

def standardize(df):
    return (df - df.mean()) / df.std()

def interpret_components(A, feature_names, top_n=2):
    interpretation = []
    for i in range(A.shape[1]):
        col = A[:, i]
        top_indices = np.argsort(np.abs(col))[::-1][:top_n]
        top_features = [feature_names[j] for j in top_indices]
        interpretation.append(f"F{i+1}: найбільше впливають {', '.join(top_features)}")
    return interpretation

def plot_scree(eigvals, task_name):
    plt.figure(figsize=(6, 4))
    plt.plot(range(1, len(eigvals)+1), eigvals, marker='o')
    plt.title(f"Графік кам’янистого осипу — {task_name}")
    plt.xlabel("Номер компоненти")
    plt.ylabel("Власне число")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"results/pr5_{task_name}_scree.png")
    plt.close()

def principal_component_analysis(df, task_name):
    Z = standardize(df)
    R = Z.corr()

    eigvals, eigvecs = np.linalg.eig(R)
    idx = eigvals.argsort()[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    A = eigvecs @ np.diag(np.sqrt(eigvals))
    A = np.real(A)

    F = np.array(Z @ A)
    F_df = pd.DataFrame(F, columns=[f'F{i+1}' for i in range(F.shape[1])], index=Z.index)

    # Інтерпретація компонент
    component_labels = interpret_components(A, df.columns.tolist())
    plot_scree(eigvals, task_name)

    md = f"# Практична робота 5 — Метод головних компонент\n"
    md += f"## Завдання: {task_name}\n\n"
    md += f"### 📊 Вхідні дані\n\n```csv\n{df.to_csv(index=False)}\n```\n"
    md += f"### 📐 Стандартизовані значення\n\n```csv\n{Z.round(3).to_csv(index=False)}\n```\n"
    md += f"### 🔗 Матриця кореляцій\n\n```csv\n{R.round(3).to_csv()}\n```\n"
    md += f"### 📈 Власні числа\n\n```text\n{eigvals.round(3)}\n```\n"
    md += f"### 🧮 Матриця факторного відображення (A)\n\n```csv\n{pd.DataFrame(A, columns=[f'F{i+1}' for i in range(A.shape[1])], index=df.columns).round(3).to_csv()}\n```\n"
    md += "### 🧠 Значення головних компонент (F)\n\n```csv\n"
    md += F_df.round(3).to_csv(index=False, header=True)
    md += "```\n"
    md += "### 🧩 Інтерпретація головних компонент\n"
    for label in component_labels:
        md += f"- {label}\n"
    md += f"\n![Графік кам’янистого осипу](pr5_{task_name}_scree.png)\n"
    md += f"### 📌 Висновки\n- Найбільш значущі ознаки мають найбільші вагові коефіцієнти у перших компонентах.\n- Сума власних чисел ≈ кількість ознак: пояснення дисперсії повне.\n"

    with open(f"results/pr5_{task_name}_principal-component.md", "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    for task in tasks:
        df = pd.read_csv(f"data/{task['filename']}")
        df_numeric = df.drop(columns=[df.columns[0]])
        principal_component_analysis(df_numeric, task['name'])