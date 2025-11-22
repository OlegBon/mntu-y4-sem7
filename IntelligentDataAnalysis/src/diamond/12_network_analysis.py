import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Налаштування шляху до файлів
DATA_FILE = os.path.join("data", "diamond", "diamonds_dataset.csv")
RESULTS_DIR = os.path.join("results", "diamond")
REPORT_FILE = os.path.join(RESULTS_DIR, "12_network_analysis_report.md")
PLOT_FILE = os.path.join(RESULTS_DIR, "12_expert_clarity_graph.png")
PLOT_BUBBLE_FILE = os.path.join(RESULTS_DIR, "12_expert_clarity_graph_bubble.png")

# Створення папки для результатів, якщо її не існує
os.makedirs(RESULTS_DIR, exist_ok=True)

df = pd.read_csv(DATA_FILE)

# Побудова двочасткового графа "Експерт <-> Чистота"
G = nx.Graph()

# Словники для імен
CLARITY_MAP = {1: 'IF', 2: 'VVS1', 3: 'VVS2', 4: 'VS1', 5: 'VS2', 6: 'SI1', 7: 'SI2', 8: 'P1', 9: 'P2', 10: 'P3'}
EXPERT_MAP = {1: 'Expert_1', 2: 'Expert_2', 3: 'Expert_3', 4: 'Expert_4', 5: 'Expert_5'}

print("Будуємо граф 'Експерт <-> Чистота'")

# Створюємо списки вузлів для графа
expert_nodes = [EXPERT_MAP[i] for i in EXPERT_MAP.keys()]
clarity_nodes = [CLARITY_MAP[i] for i in CLARITY_MAP.keys()]

G.add_nodes_from(expert_nodes, bipartite=0, type='expert')
G.add_nodes_from(clarity_nodes, bipartite=1, type='clarity')

# Мапуємо ID на імена прямо в DataFrame
df['expert_node'] = df['expert_id'].map(EXPERT_MAP)
df['clarity_node'] = df['clarity_grade'].map(CLARITY_MAP)

# Групуємо та рахуємо вагу (кількість) кожного унікального зв'язку
edge_weights = df.groupby(['expert_node', 'clarity_node']).size().reset_index(name='weight')

# print(f"!!! ПЕРЕВІРКА СУМИ ВАГ: {edge_weights['weight'].sum()} !!!") # Має дорівнювати кількості рядків у df

print("Рахуємо вагу ребер")
# print(edge_weights.to_string()) # Розкоментувати, щоб побачити результат

# Створюємо список кортежів для NetworkX
# (expert_node, clarity_node, weight_value)
weighted_edges = [
    (row['expert_node'], row['clarity_node'], row['weight']) 
    for index, row in edge_weights.iterrows()
]

# Додаємо всі пораховані ребра та їх ваги в граф одним махом
G.add_weighted_edges_from(weighted_edges)

print(f"Граф 'Експерт <-> Чистота' побудовано (методом groupby)")
print(f"Загальна кількість вузлів: {G.number_of_nodes()}")
print(f"Загальна кількість зв'язків: {G.number_of_edges()}")

# Аналіз графа за допомогою алгоритмів обходу (Traversal Algorithms)
print("\nЗастосування алгоритмів обходу (Traversal)")

# Алгоритм 1: Обхід в глибину (DFS) -> Пошук компонент зв'язності
print("\nПошук компонент зв'язності (спільнот):")
components = list(nx.connected_components(G))
components_result = f"Знайдено {len(components)} окремих компонент(и) у графі."
print(components_result)

# Алгоритм 2: Обхід в ширину (BFS) -> Пошук довжини найкоротшого шляху (приклад між двома експертами)
start_node = 'Expert_1'
end_node = 'Expert_5'
path_result = ""
try:
    # Замість одного шляху, знайдемо його довжину
    length = nx.shortest_path_length(G, source=start_node, target=end_node)
    
    path_result = (
        f"Найкоротший шлях між будь-якими двома експертами (напр., {start_node} та {end_node}) має довжину **{length} кроки**.\n\n"
        f"(Це підтверджує, що граф є повністю зв'язаним. Будь-який експерт пов'язаний з будь-яким іншим експертом "
        f"через 'одне рукостискання' - тобто через хоча б одну спільну категорію чистоти, над якою вони обидва працювали.)\n"
    )
    print(f"Довжина шляху між {start_node} та {end_node}: {length}")

except nx.NetworkXNoPath:
    path_result = f"Шлях між {start_node} та {end_node} не знайдено.\n"
    print(path_result)

# Візуалізація графа
print(f"\nЗбереження графа у файл: {PLOT_FILE}")
plt.figure(figsize=(14, 10))

# Розділяємо вузли на 2 групи для візуалізації
pos = dict()
pos.update((node, (1, i)) for i, node in enumerate(expert_nodes)) # Експерти зліва
pos.update((node, (2, i * 0.5)) for i, node in enumerate(clarity_nodes)) # Чистота справа

# Малюємо вузли
nx.draw_networkx_nodes(G, pos, nodelist=expert_nodes, node_color='skyblue', node_size=3000)
nx.draw_networkx_nodes(G, pos, nodelist=clarity_nodes, node_color='lightgreen', node_size=3000)
# Малюємо ребра
# nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
max_weight = max(nx.get_edge_attributes(G, 'weight').values())
edge_widths = [G[u][v]['weight'] / max_weight * 5 + 0.5 for u, v in G.edges()] # Масштабуємо ваги для товщини 
# Малюємо ребра з динамічною товщиною
nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.7, edge_color='gray')
# Малюємо вагу ребер
edge_labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
# Малюємо мітки вузлів
nx.draw_networkx_labels(G, pos, font_size=10)

plt.title("Двочастковий граф 'Експерт <-> Чистота'", size=16)
plt.axis('off') # Вимкнути осі
plt.savefig(PLOT_FILE)
plt.close()
print("Візуалізацію збережено.")

# Візуалізація бульбашкового графа
print(f"\nЗбереження бульбашкового графа у файл: {PLOT_BUBBLE_FILE}")
plt.figure(figsize=(14, 14))

# Розраховуємо розмір вузлів на основі сумарної ваги (Weighted Degree)
node_degrees = dict(G.degree(weight='weight'))
# Масштабування розміру (емпірично підібраний коефіцієнт * 20 + мінімальний розмір)
node_sizes = [node_degrees[node] * 20 + 500 for node in G.nodes()]

# Малюємо вузли з динамічним розміром ("бульбашки")
nx.draw_networkx_nodes(G, pos, 
                       nodelist=G.nodes(), 
                       node_color=['skyblue' if n in expert_nodes else 'lightgreen' for n in G.nodes()],
                       node_size=node_sizes, 
                       alpha=0.8)

# Малюємо ребра (так само динамічна товщина)
nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, edge_color='gray')

# Додаємо підписи з кількістю (сумарною вагою) всередині або поруч з вузлами
labels_with_counts = {node: f"{node}\n({node_degrees[node]})" for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=labels_with_counts, font_size=8)

plt.title("Бульбашковий граф (Розмір вузла = Сумарна кількість оцінок)", size=16)
plt.axis('off')
plt.savefig(PLOT_BUBBLE_FILE)
plt.close()
print("Бульбашкову візуалізацію збережено.")

# Генерація звіту
print(f"Генерація звіту: {REPORT_FILE}")
with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.write(f"# Звіт з аналізу графа (Самостійна робота №12)\n\n")
    # ... (інфо про граф) ...
    
    f.write("## 2. Аналіз за допомогою алгоритмів обходу (Traversal)\n\n")
    
    f.write("### 2.1. Компоненти зв'язності (на основі DFS)\n\n")
    f.write(components_result + "\n")
    if len(components) > 1:
        f.write("Це означає, що існують ізольовані групи експертів/характеристик...\n")
    else:
        f.write("Це означає, що всі експерти та характеристики пов'язані в єдину мережу.\n\n")

    f.write("### 2.2. Аналіз найкоротшого шляху (на основі BFS)\n\n")
    f.write(path_result + "\n")
    f.write("\n## 3. Візуалізація графа\n\n")
    f.write("### 3.1. Візуалізація (Товщина ребер = Сила зв'язку)\n\n")
    f.write(f"![Візуалізація графа](12_expert_clarity_graph.png)\n\n")
    
    f.write("### 3.2. Бульбашкова візуалізація (Розмір вузла = Загальна активність)\n\n")
    f.write("На цьому графіку розмір кола пропорційний загальній кількості оцінок, зроблених експертом (або отриманих категорією чистоти).\n\n")
    f.write(f"![Бульбашкова візуалізація](12_expert_clarity_graph_bubble.png)\n")

print("Аналіз завершено")