import numpy as np

def pagerank(adj_matrix, d=0.85, max_iter=100, tol=1e-6):
    n = adj_matrix.shape[0]
    out_degrees = adj_matrix.sum(axis=1)
    M = np.zeros((n, n), dtype=float)

    for i in range(n):
        if out_degrees[i] > 0:
            M[i] = adj_matrix[i] / out_degrees[i]
        else:
            M[i] = np.ones(n) / n

    M = M.T
    v = np.ones(n) / n
    teleport = np.ones(n) / n

    for _ in range(max_iter):
        v_next = d * M.dot(v) + (1 - d) * teleport
        if np.linalg.norm(v_next - v, 1) < tol:
            break
        v = v_next

    return v

if __name__ == "__main__":
    adj = np.array([
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 0, 1, 0],
    ])

    print(pagerank(adj))