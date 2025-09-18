import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
import os

tasks = [
    {'name': 'z1', 'filename': 'pr2_z1_data.csv'},
    {'name': 'z2', 'filename': 'pr2_z2_data.csv'},
    {'name': 'z3', 'filename': 'pr2_z3_data.csv', 'weights': [0.3, 0.7]},
    {'name': 'z4', 'filename': 'pr2_z4_data.csv', 'metric': 'cityblock'},
    {'name': 'z5', 'filename': 'pr2_z5_data.csv', 'metric': 'jaccard'},
]

for task in tasks:
    print(f"\n🔄 Обробка завдання {task['name']}")

    data_path = os.path.join('data', task['filename'])
    result_path = os.path.join('results', f"pr2_{task['name']}_euclidean_matrix.csv")

    df = pd.read_csv(data_path)
    data = df.drop(columns=['ID']).values

    # Вибір метрики
    if 'weights' in task:
        weights = np.array(task['weights'])
        def weighted_euclidean(u, v):
            return np.sqrt(np.sum(weights * (u - v)**2))
        distance_matrix = squareform(pdist(data, metric=weighted_euclidean))
    elif 'metric' in task:
        distance_matrix = squareform(pdist(data, metric=task['metric']))
    else:
        distance_matrix = squareform(pdist(data, metric='euclidean'))

    distance_matrix = np.round(distance_matrix, 2)

    object_labels = df['ID'].astype(str).tolist()
    dist_df = pd.DataFrame(distance_matrix, index=object_labels, columns=object_labels)
    dist_df.index.name = 'ID'

    dist_df.to_csv(result_path, float_format='%.2f')
    print(dist_df)