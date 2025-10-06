import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Вхідні змінні
# Температура (temp): 10-80
temp = ctrl.Antecedent(np.arange(10, 81, 1), 'temp')
# Напір (head): 0-1
head = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'head')
# Вихідна змінна
valve = ctrl.Consequent(np.arange(-90, 91, 1), 'valve')

# Функції належності
# Температура (холодна, середня, гаряча)
temp['cold'] = fuzz.trimf(temp.universe, [10, 20, 35])
temp['mid'] = fuzz.trimf(temp.universe, [30, 35, 40])
temp['hot'] = fuzz.trimf(temp.universe, [40, 50, 80])

# Напір (малий, нормальний, великий)
head['small'] = fuzz.trimf(head.universe, [0, 0.1, 0.3])
head['norm'] = fuzz.trimf(head.universe, [0.25, 0.5, 0.75])
head['big'] = fuzz.trimf(head.universe, [0.6, 0.8, 1])

# Кут повороту крана (відкрити сильно, відкрити слабо, нормально, закрити слабо, закрити сильно)
valve['open_q'] = fuzz.trimf(valve.universe, [-90, -70, -50])
valve['open_s'] = fuzz.trimf(valve.universe, [-60, -30, -10])
valve['norm'] = fuzz.trimf(valve.universe, [-15, 0, 15])
valve['close_s'] = fuzz.trimf(valve.universe, [10, 30, 60])
valve['close_q'] = fuzz.trimf(valve.universe, [50, 70, 90])

# Правила
# 1. Якщо температура холодна і напір малий, тоді відкрити сильно
rule1 = ctrl.Rule(temp['cold'] & head['small'], valve['open_q'])
# 2. Якщо температура середня і напір нормальний, тоді нормально
rule2 = ctrl.Rule(temp['mid'] & head['norm'], valve['norm'])
# 3. Якщо температура гаряча і напір великий, тоді закрити сильно
rule3 = ctrl.Rule(temp['hot'] & head['big'], valve['close_q'])
# 4. Якщо температура гаряча і напір нормальний, тоді закрити слабо
rule4 = ctrl.Rule(temp['hot'] & head['norm'], valve['close_s'])
# 5. Якщо температура середня і напір великий, тоді закрити слабо
rule5 = ctrl.Rule(temp['mid'] & head['big'], valve['close_s'])
# 6. Якщо температура холодна і напір нормальний, тоді відкрити слабо
rule6 = ctrl.Rule(temp['cold'] & head['norm'], valve['open_s'])

# Система керування
system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
sim = ctrl.ControlSystemSimulation(system)

# Вхідні значення
input_temp = 75
input_head = 0.9

def interpret_valve_output(value):
    
    if value <= -60:
        return "відкрити сильно"
    elif -60 < value <= -30:
        return "відкрити слабо"
    elif -30 < value <= 30:
        return "нормально"
    elif 30 < value <= 60:
        return "закрити слабо"
    else:
        return "закрити сильно"

# Передача значень у симуляцію
sim.input['temp'] = input_temp
sim.input['head'] = input_head
sim.compute()

# Перевірка, чи є результат
if 'valve' in sim.output:
    output_value = sim.output['valve']
    action_text = interpret_valve_output(output_value)
    print(f"Кут повороту крана при temp={input_temp} і head={input_head}: {action_text} (кут {output_value:.0f} град.)")
else:
    # Дефолтне повідомлення або значення
    print(f"Кут повороту крана при temp={input_temp} і head={input_head}: немає активного правила для цієї комбінації.")

# Виведення правил
rules = [rule1, rule2, rule3, rule4, rule5, rule6]

print("\nСписок правил нечіткої системи:")
for i, rule in enumerate(rules, start=1):
    antecedents = " і ".join([term.label for term in rule.antecedent_terms])
    consequent = rule.consequent[0].term.label
    print(f"{i}. Якщо {antecedents}, тоді {consequent}")