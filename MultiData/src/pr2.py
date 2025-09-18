import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

df = pd.read_csv('data/pr2_z1_data.csv')

data = df[['X1', 'X2']].values

distance_matrix = squareform(pdist(data, metric='euclidean'))

distance_matrix = np.round(distance_matrix, 2)

object_labels = df['ID'].astype(str).tolist()
dist_df = pd.DataFrame(distance_matrix, index=object_labels, columns=object_labels)
dist_df.index.name = 'ID'

dist_df.to_csv('results/pr2_z1_euclidean_matrix.csv', float_format='%.2f')

print(dist_df)