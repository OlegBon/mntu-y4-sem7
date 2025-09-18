import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
import os

tasks = [
    {'name': 'z1', 'filename': 'pr2_z1_data.csv'},
    {'name': 'z2', 'filename': 'pr2_z2_data.csv'},
    # Додай інші завдання тут
]

for task in tasks:
    print(f"\n🔄 Обробка завдання {task['name']}")

    data_path = os.path.join('data', task['filename'])
    result_path = os.path.join('results', f"pr2_{task['name']}_euclidean_matrix.csv")

    df = pd.read_csv(data_path)

    data = df[['X1', 'X2']].values
    distance_matrix = squareform(pdist(data, metric='euclidean'))
    distance_matrix = np.round(distance_matrix, 2)

    object_labels = df['ID'].astype(str).tolist()
    dist_df = pd.DataFrame(distance_matrix, index=object_labels, columns=object_labels)
    dist_df.index.name = 'ID'

    dist_df.to_csv(result_path, float_format='%.2f')
    print(dist_df)