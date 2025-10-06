import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import random
import lorem

# === Вхідні змінні ===
# low, medium, high
emotion = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'emotion')
# short, medium, long
word_count = ctrl.Antecedent(np.arange(0, 201, 1), 'word_count')
# fast, normal, slow
fill_time = ctrl.Antecedent(np.arange(0, 301, 1), 'fill_time')

# === Вихідна змінна ===
response_type = ctrl.Consequent(np.arange(0, 101, 1), 'response_type')

# === Функції належності ===
emotion['low'] = fuzz.trimf(emotion.universe, [0.0, 0.0, 0.3])
emotion['medium'] = fuzz.trimf(emotion.universe, [0.2, 0.5, 0.8])
emotion['high'] = fuzz.trimf(emotion.universe, [0.7, 1.0, 1.0])

word_count['short'] = fuzz.trimf(word_count.universe, [0, 0, 50])
word_count['medium'] = fuzz.trimf(word_count.universe, [30, 100, 150])
word_count['long'] = fuzz.trimf(word_count.universe, [120, 200, 200])

fill_time['fast'] = fuzz.trimf(fill_time.universe, [0, 0, 60])
fill_time['normal'] = fuzz.trimf(fill_time.universe, [40, 150, 220])
fill_time['slow'] = fuzz.trimf(fill_time.universe, [180, 300, 300])

response_type['automatic'] = fuzz.trimf(response_type.universe, [0, 0, 30])
response_type['manual'] = fuzz.trimf(response_type.universe, [20, 50, 80])
response_type['urgent'] = fuzz.trimf(response_type.universe, [70, 100, 100])

# === Правила ===
# Створення правил на основі комбінацій вхідних змінних 3x3x3 = 27
rules = []

for e in ['low', 'medium', 'high']:
    for w in ['short', 'medium', 'long']:
        for t in ['fast', 'normal', 'slow']:
            # Логіка вибору типу відповіді
            if e == 'high' and w == 'short' and t == 'fast':
                response = 'urgent'
            elif e == 'high' and w == 'short':
                response = 'manual'
            elif e == 'high':
                response = 'manual'
            elif e == 'medium' and w == 'short' and t == 'fast':
                response = 'urgent'
            elif e == 'medium' and w == 'medium' and t == 'normal':
                response = 'manual'
            elif e == 'medium' and w == 'long':
                response = 'automatic'
            elif e == 'low' and w == 'long' and t == 'slow':
                response = 'automatic'
            elif e == 'low' and w == 'short':
                response = 'manual'
            elif e == 'low' and t == 'fast':
                response = 'automatic'
            else:
                response = 'manual'  # дефолтна логіка

            rules.append(ctrl.Rule(emotion[e] & word_count[w] & fill_time[t], response_type[response]))

# === Система керування ===
system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

# === Моки ===
emotion_score = round(random.uniform(0, 1), 2)
word_count_value = random.randint(0, 200)
fill_time_value = random.randint(0, 300)

# === Рандомний текст ===
# words = ["дякую", "помилка", "не працює", "будь ласка", "терміново", "чудово", "жахливо", "поясніть", "не можу", "допоможіть"]
# random_text = " ".join(random.choices(words, k=word_count_value))
random_text = lorem.text()

# === Передача значень ===
sim.input['emotion'] = emotion_score
sim.input['word_count'] = word_count_value
sim.input['fill_time'] = fill_time_value
sim.compute()

# === Інтерпретація виходу ===
def interpret_response(value):
    if value <= 30:
        return "автоматична відповідь"
    elif value <= 70:
        return "ручна відповідь"
    else:
        return "термінова відповідь"

response_value = sim.output['response_type']
response_text = interpret_response(response_value)

# === Вивід результату ===
print("=== Результат форми зворотного зв’язку ===")
print(f"Емоційність: {emotion_score}")
print(f"Кількість слів: {word_count_value}")
print(f"Час заповнення: {fill_time_value} сек")
print(f"Текст: {random_text[:200]}{'...' if word_count_value > 30 else ''}")
print(f"Тип відповіді: {response_text} ({response_value:.1f})")