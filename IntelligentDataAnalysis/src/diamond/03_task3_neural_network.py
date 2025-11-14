import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from datetime import datetime
import os
import warnings

print("Старт")

# Налаштування шляхів
DATA_FILE = os.path.join("data", "diamond", "diamonds_dataset.csv")
RESULTS_DIR = os.path.join("results", "diamond")

PLOT_FILE = "03_neural_network_confusion_matrix.png"
REPORT_FILE = os.path.join(RESULTS_DIR, "03_neural_network_report.md")
METRICS_FILE = os.path.join(RESULTS_DIR, "03_neural_network_metrics.txt")

# Створюємо повні шляхи
PLOT_PATH = os.path.join(RESULTS_DIR, PLOT_FILE)
REPORT_PATH = os.path.join(RESULTS_DIR, REPORT_FILE)
METRICS_PATH = os.path.join(RESULTS_DIR, METRICS_FILE)

os.makedirs(RESULTS_DIR, exist_ok=True)
# Ігноруємо попередження про те, що модель не зійшлася (може бути на складних даних)
warnings.filterwarnings('ignore', category=Warning) 

# Завантаження даних
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"ПОМИЛКА: Файл {DATA_FILE} не знайдено.")
    print("Будь ласка, спочатку запустіть скрипт '00_generate_dataset.py'")
    exit()

features_list = ['carat_weight', 'color_grade', 'clarity_grade', 'cut_grade']
target_variable = 'is_investment_grade'
class_names_list = ['Not Investment', 'Investment Grade']

X = df[features_list]
y = df[target_variable]

print(f"Дані завантажено. Будуємо Нейромережу для: '{target_variable}'")

# Масштабування даних є критично важливим для нейронних мереж
print("Масштабування даних (StandardScaler)...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Побудова та навчання моделі
# Використовуємо параметри з Варіанту 1 
model = MLPClassifier(
    hidden_layer_sizes=(3,), # 1 прихований шар з 3-ма нейронами
    activation='logistic', # Логістична сигмоїдна функція
    max_iter=1000, # Збільшимо кількість ітерацій
    random_state=42
)
print("Навчання нейронної мережі")
model.fit(X_scaled, y) # Навчаємо на масштабованих даних

y_pred = model.predict(X_scaled)
accuracy = accuracy_score(y, y_pred)

print(f"Модель навчено. Точність (Accuracy): {accuracy:.4f}")

# Збереження метрик
print(f"Збереження метрик у {METRICS_FILE}")
report = classification_report(y, y_pred, target_names=class_names_list, zero_division=0)
conf_matrix = confusion_matrix(y, y_pred)

with open(METRICS_FILE, "w", encoding="utf-8") as f:
    f.write(f"--- Результати моделі MLPClassifier (Варіант 1: 3-1, logistic) ---\n\n")
    f.write(f"Accuracy: {accuracy:.4f}\n\n")
    f.write("--- Classification Report ---\n")
    f.write(report + "\n")
    f.write("\n--- Confusion Matrix ---\n")
    f.write(str(conf_matrix) + "\n")

# Візуалізація матриці помилок
print(f"Збереження візуалізації матриці помилок у {PLOT_PATH}")
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, 
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=class_names_list, 
            yticklabels=class_names_list)
plt.title(f"Матриця помилок: Нейронна мережа (Точність: {accuracy:.3f})")
plt.ylabel('Справжній клас (True Label)')
plt.xlabel('Прогнозований клас (Predicted Label)')
plt.savefig(PLOT_PATH)
plt.close()

# Генерація звіту
print(f"Генерація звіту у {REPORT_FILE}")
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(f"# Звіт з Самостійної роботи №3 (Завдання 3): Нейронна мережа\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write(f"**Мета:** Побудувати Нейронну мережу (`MLPClassifier`) для класифікації `{target_variable}` "
            f"та порівняти її ефективність з Деревом рішень.\n\n")
    f.write(f"**Параметри моделі (Варіант 1):** 1 прихований шар (3 нейрони), активація 'logistic'.\n\n")
    f.write("---\n\n")

    f.write("## 1. Результати моделювання\n\n")
    f.write(f"Модель `MLPClassifier` була навчена на 1000 зразках (з попереднім масштабуванням `StandardScaler`).\n\n")
    f.write(f"- **Точність (Accuracy):** `{accuracy:.4f}`\n")
    f.write(f"- **Матриця помилок:**\n```\n{conf_matrix}\n```\n\n")
    f.write(f"**Детальний звіт:**\n```\n{report}\n```\n\n")
    
    f.write("\n## 2. Візуалізація результатів\n\n")
    f.write(f"Оскільки ми використовуємо 4 ознаки (4D), ми не можемо побудувати 2D-межу класифікації, як у старій СР-3.\n")
    f.write(f"Натомість, ми візуалізуємо **Матрицю помилок (Confusion Matrix)**, яка показує точність роботи моделі.\n\n")
    f.write(f"![Візуалізація матриці помилок]({PLOT_FILE})\n\n") # <--- ОНОВЛЕНЕ ПОСИЛАННЯ
    
    f.write("## 3. Загальний висновок (Порівняння з Деревом рішень)\n\n")
    
    if accuracy == 1.0:
        f.write("Нейронна мережа, як і Дерево рішень, показала **ідеальну точність (100.0%)**. "
                "Це підтверджує, що на достатньому обсязі даних (1000 рядків) `MLPClassifier` "
                "також зміг бездоганно вивчити чіткі бізнес-правила, закладені в датасет.\n\n")
    else:
        f.write("На відміну від Дерева рішень, яке показало 100% точність, Нейронна мережа "
                f"досягла точності **{accuracy:.1%}**. \n\n"
                "Це демонструє ключову відмінність: \n"
                "1. **Дерево рішень (Завдання 2)** ідеально знаходить чіткі, порогові правила (IF `carat_weight > 1`...).\n"
                "2. **Нейронна мережа (Завдання 3)** є імовірнісною моделлю. Вона знайшла *дуже близькі* правила, "
                "але допустила кілька помилок на прикордонних значеннях.\n\n"
                "Цей результат доводить, що нейронні мережі вимагають значно більшого обсягу даних для навчання, ніж дерева рішень.\n")

print(f"\nЗвіт збережено: {REPORT_FILE}")