import numpy as np
from scipy.spatial.distance import pdist
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import re

def read_points(filename: str) -> list[tuple[int, int, int]]:
    with open(filename, 'r') as f:
        raw_data = re.findall(r'(\d+),(\d+),(\d+)', f.read())
    return raw_data

def solve_part_1(filename='input.txt'):
    data = read_points(filename)
    points = np.array(data, dtype=np.int32)

    # Safety check, input should'nt be over 1000 lines
    if len(points) > 1000: points = points[:1000]
    n = len(points)

    # Using dist^2 to avoid computing the square-root, doesn't affect the result
    dists = pdist(points, 'sqeuclidean')

    # Select only the 1000 smallest entries
    k = 1000
    closest_indices = np.argpartition(dists, k)[:k]

    # Map condensed indices (from pdist output) back to endpoint pairs (i, j)
    I, J = np.triu_indices(n, 1)   # all (i,j) from upper triangle-matrix
    i = I[closest_indices]
    j = J[closest_indices]


    rows = np.concatenate([i, j])
    cols = np.concatenate([j, i])
    # Marking the existance of edges
    data = np.ones(len(rows), dtype=np.bool_) # Bool uses less memory
    graph = coo_matrix((data, (rows, cols)), shape=(n, n))

    # Assigning nodes to their circuits/group
    _, labels = connected_components(csgraph=graph, directed=False, return_labels=True)
    _, counts = np.unique(labels, return_counts=True)

    top3 = np.sort(counts)[::-1][:3]

    if len(top3) < 3: top3 = np.pad(top3, (0, 3-len(top3)), constant_values=1)

    return np.prod(top3)


'''
We are building a Minimum Spanning Tree (MST) using Prim's algorithm 
on the complete graph with squared Euclidean distance.
'''
def solve_part_2(path: str) -> int:
    raw_points = read_points(path)

    # This is due to recent changes in the read-function
    points = [(int(x), int(y), int(z)) for (x, y, z) in raw_points]

    n = len(points)
    if n < 2:
        return 0

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]

    INF = 10**30 # Just a large number to init the distance
    in_tree = [False] * n
    best_dist = [INF] * n
    parent = [-1] * n

    best_dist[0] = 0

    max_edge_dist = -1
    max_edge_u = -1
    max_edge_v = -1

    for _ in range(n):
        # pick the not-in-tree node with smallest best_dist
        u = -1
        u_dist = INF
        for i in range(n):
            if not in_tree[i] and best_dist[i] < u_dist:
                u_dist = best_dist[i]
                u = i

        in_tree[u] = True

        # Keeping track of the largest distance, which will be the last 
        # node that we will connect
        if parent[u] != -1 and u_dist > max_edge_dist:
            max_edge_dist = u_dist
            max_edge_u = u
            max_edge_v = parent[u]

        # update best_dist for all remaining nodes
        xu, yu, zu = xs[u], ys[u], zs[u]
        for v in range(n):
            if in_tree[v]:
                continue
            dx = xu - xs[v]
            dy = yu - ys[v]
            dz = zu - zs[v]
            d2 = dx*dx + dy*dy + dz*dz  # squared distance
            if d2 < best_dist[v]:
                best_dist[v] = d2
                parent[v] = u

    return xs[max_edge_u] * xs[max_edge_v]


if __name__ == "__main__":
    print("Solving day 8!")
    print("Solution for part 1: ", solve_part_1())
    print("Solution for part 2: ", solve_part_2("input.txt"))



