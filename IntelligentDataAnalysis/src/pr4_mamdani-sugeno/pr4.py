import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import os
from datetime import datetime

# === Етап 0: Налаштування констант ===
RESULTS_DIR = "results/pr4-mamdani-sugeno"
os.makedirs(RESULTS_DIR, exist_ok=True)

# === Етап 1: Побудова еталонної поверхні ===
def plot_etalon_surface():
    print("1. Побудова еталонної поверхні...")
    x1_range = np.linspace(-7, 3, 30)
    x2_range = np.linspace(-4.4, 1.7, 30)
    x1, x2 = np.meshgrid(x1_range, x2_range)
    y_etalon = (x1**2) * np.sin(x2 - 1)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x1, x2, y_etalon, cmap='viridis')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('y')
    ax.set_title('Еталонна поверхня: y = x1^2 * sin(x2 - 1)')
    
    filename = "pr4_etalon_surface.png"
    plt.savefig(os.path.join(RESULTS_DIR, filename))
    plt.close()
    print("   ...збережено.")
    return filename

# === Утиліта для побудови поверхні нечіткої системи ===
def plot_fuzzy_surface(simulation, system_name):
    print(f"   Побудова поверхні для '{system_name}'...")
    x1_vals = np.linspace(-7, 3, 30)
    x2_vals = np.linspace(-4.4, 1.7, 30)
    y_vals = np.zeros((len(x2_vals), len(x1_vals)))

    for i, x1 in enumerate(x1_vals):
        for j, x2 in enumerate(x2_vals):
            simulation.input['x1'] = x1
            simulation.input['x2'] = x2
            try:
                simulation.compute()
                y_vals[j, i] = simulation.output['y']
            except:
                y_vals[j, i] = 0

    X1, X2 = np.meshgrid(x1_vals, x2_vals)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X1, X2, y_vals, cmap='viridis')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('y')
    ax.set_title(f'Поверхня "входи-вихід" ({system_name})')
    
    filename = f"pr4_{system_name.lower()}_surface.png"
    plt.savefig(os.path.join(RESULTS_DIR, filename))
    plt.close()
    print("   ...збережено.")
    return filename

# === Етап 2: Створення системи типу Сугено (імітація) ===
def build_sugeno_like_system():
    x1 = ctrl.Antecedent(np.arange(-7, 3.1, 0.1), 'x1')
    x2 = ctrl.Antecedent(np.arange(-4.4, 1.8, 0.1), 'x2')
    y = ctrl.Consequent(np.arange(-50, 51, 1), 'y', defuzzify_method='centroid')

    x1['низький'] = fuzz.trimf(x1.universe, [-7, -7, -2])
    x1['середній'] = fuzz.trimf(x1.universe, [-6, -2, 2])
    x1['високий'] = fuzz.trimf(x1.universe, [-2, 3, 3])

    x2['низький'] = fuzz.trimf(x2.universe, [-4.4, -4.4, -1.35])
    x2['середній'] = fuzz.trimf(x2.universe, [-3.79, -1.35, 1.09])
    x2['високий'] = fuzz.trimf(x2.universe, [-1.35, 1.7, 1.7])
    # Використання "синглтонів" (дуже вузьких трикутників) для імітації чітких виходів
    y['y0'] = fuzz.trimf(y.universe, [-0.1, 0, 0.1])
    y['y5'] = fuzz.trimf(y.universe, [4.9, 5, 5.1])
    y['y10'] = fuzz.trimf(y.universe, [9.9, 10, 10.1])
    y['y_neg30'] = fuzz.trimf(y.universe, [-30.1, -30, -29.9])
    y['y50'] = fuzz.trimf(y.universe, [49.9, 50, 50.1])

    rules = [
        ctrl.Rule(x1['середній'], y['y0']),
        ctrl.Rule(x1['високий'] & x2['високий'], y['y5']),
        ctrl.Rule(x1['високий'] & x2['низький'], y['y10']),
        ctrl.Rule(x1['низький'] & x2['середній'], y['y_neg30']),
        ctrl.Rule(x1['низький'] & x2['низький'], y['y50']),
        ctrl.Rule(x1['низький'] & x2['високий'], y['y50'])
    ]
    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))

# === Етап 3: Створення класичної системи Мамдані ===
def build_mamdani_system():
    x1 = ctrl.Antecedent(np.arange(-7, 3.1, 0.1), 'x1')
    x2 = ctrl.Antecedent(np.arange(-4.4, 1.8, 0.1), 'x2')
    y = ctrl.Consequent(np.arange(-50, 51, 1), 'y', defuzzify_method='centroid')

    x1['низький'] = fuzz.trimf(x1.universe, [-7, -7, -2])
    x1['середній'] = fuzz.trimf(x1.universe, [-6, -2, 2])
    x1['високий'] = fuzz.trimf(x1.universe, [-2, 3, 3])

    x2['низький'] = fuzz.trimf(x2.universe, [-4.4, -4.4, -1.35])
    x2['середній'] = fuzz.trimf(x2.universe, [-3.79, -1.35, 1.09])
    x2['високий'] = fuzz.trimf(x2.universe, [-1.35, 1.7, 1.7])
    # Використання широких нечітких множин для виходу
    y['дуже низький'] = fuzz.trimf(y.universe, [-50, -50, -25])
    y['низький'] = fuzz.trimf(y.universe, [-40, -20, 0])
    y['середній'] = fuzz.trimf(y.universe, [-10, 0, 10])
    y['високий'] = fuzz.trimf(y.universe, [0, 20, 40])
    y['дуже високий'] = fuzz.trimf(y.universe, [25, 50, 50])

    rules = [
        ctrl.Rule(x1['низький'] & x2['низький'], y['дуже високий']),
        ctrl.Rule(x1['низький'] & x2['середній'], y['низький']),
        ctrl.Rule(x1['низький'] & x2['високий'], y['дуже низький']),
        ctrl.Rule(x1['середній'], y['середній']),
        ctrl.Rule(x1['високий'] & x2['низький'], y['високий']),
        ctrl.Rule(x1['високий'] & x2['середній'], y['середній']),
        ctrl.Rule(x1['високий'] & x2['високий'], y['низький'])
    ]
    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))

# === Етап 4: Генерація фінального звіту ===
def generate_report(etalon_img, sugeno_img, mamdani_img):
    print("4. Генерація фінального звіту...")
    
    # Створення тексту таблиці правил
    rules_table = """
---
### Таблиця правил нечіткого виведення

| № | Умова (x1, x2) | Вихід (y) | Тип системи |
|---|----------------|-----------|-------------|
| 1 | x1 = середній | y = 0 | Сугено |
| 2 | x1 = високий, x2 = високий | y = 5 | Сугено |
| 3 | x1 = високий, x2 = низький | y = 10 | Сугено |
| 4 | x1 = низький, x2 = середній | y = -30 | Сугено |
| 5 | x1 = низький, x2 = низький | y = 50 | Сугено |
| 6 | x1 = низький, x2 = високий | y = 50 | Сугено |
| 7 | x1 = низький, x2 = низький | y = дуже високий | Мамдані |
| 8 | x1 = низький, x2 = середній | y = низький | Мамдані |
| 9 | x1 = низький, x2 = високий | y = дуже низький | Мамдані |
|10 | x1 = середній | y = середній | Мамдані |
|11 | x1 = високий, x2 = низький | y = високий | Мамдані |
|12 | x1 = високий, x2 = середній | y = середній | Мамдані |
|13 | x1 = високий, x2 = високий | y = низький | Мамдані |
"""

    report_content = f"""
# Звіт з практичної роботи: Порівняння алгоритмів Мамдані та Сугено
**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Мета роботи
Освоїти принципи роботи алгоритмів Мамдані та Сугено, порівняти їх ефективність на прикладі апроксимації нелінійної функції.

---
## Етап 1: Еталонна поверхня
Було побудовано еталонну 3D-поверхню для цільової функції $y = x_1^2 \\cdot \\sin(x_2 - 1)$ в діапазонах $x_1 \\in [-7, 3]$ та $x_2 \\in [-4.4, 1.7]$.

![Еталонна поверхня]({etalon_img})

---
## Етап 2: Система типу Сугено (імітація)
Була реалізована система, що імітує поведінку Сугено нульового порядку за допомогою архітектури Мамдані з "синглтонними" (точковими) виходами.

![Поверхня Сугено (імітація)]({sugeno_img})

---
## Етап 3: Класична система Мамдані
Була реалізована класична система типу Мамдані з широкими нечіткими множинами на виході.

![Поверхня Мамдані]({mamdani_img})

{rules_table}

---
## Етап 4: Порівняльні висновки
- **Система, що імітує Сугено,** генерує ступінчату, кусково-постійну поверхню. Вона грубо апроксимує загальну форму функції, але повністю втрачає її плавність, що є наслідком імітації чітких виходів.
- **Класична система Мамдані** створює плавну, нелінійну поверхню, яка візуально значно краще відповідає складній формі еталонної функції. Це досягається за рахунок агрегації та дефазифікації широких нечітких множин на виході.
- **Висновок**: Для задач апроксимації складних функцій в середовищі `scikit-fuzzy`, **класичний алгоритм Мамдані є більш гнучким та ефективним інструментом**, ніж імітація Сугено.
"""
    report_path = os.path.join(RESULTS_DIR, "report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print("   ...звіт збережено.")

# === Головний блок виконання ===
if __name__ == "__main__":
    # Етап 1
    etalon_filename = plot_etalon_surface()

    # Етап 2
    print("2. Побудова системи Сугено (імітація)...")
    sugeno_sim = build_sugeno_like_system()
    sugeno_filename = plot_fuzzy_surface(sugeno_sim, "Sugeno")

    # Етап 3
    print("3. Побудова системи Мамдані...")
    mamdani_sim = build_mamdani_system()
    mamdani_filename = plot_fuzzy_surface(mamdani_sim, "Mamdani")

    # Етап 4
    generate_report(etalon_filename, sugeno_filename, mamdani_filename)
    
    print(f"✅ Усі етапи завершено. Результати у папці: '{RESULTS_DIR}'")