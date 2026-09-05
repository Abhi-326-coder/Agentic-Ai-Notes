import faiss
import numpy as np

vectors = np.array([
    [0.1, 0.2, 0.3],
    [0.2, 0.3, 0.4],
    [0.9, 0.8, 0.7]
], dtype="float32")

index = faiss.IndexFlatL2(3)

index.add(vectors)

query = np.array([
    [0.1, 0.2, 0.25]
], dtype="float32")

distances, indices = index.search(query, k=2)

print(distances)
print(indices)