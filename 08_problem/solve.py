import heapq

# Implementing Union-Find data structure to represent the groups of circuits,
# because the main operations needed are merge and find.
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, a: int) -> int:
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a: int, b: int) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        # Connect the smaller tree/circuit to the bigger one
        # to make search faster
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

# save input-file as a list
def read_points(path: str) -> list[tuple[int, int, int]]:
    pts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            x_str, y_str, z_str = s.split(",")
            pts.append((int(x_str), int(y_str), int(z_str)))
    return pts

def k_smallest_pairs(points: list[tuple[int, int, int]], k: int):
    n = len(points)
    if n < 2:
        return []

    # We limit the amounts of lookups to save memory usage
    heap = []
    heappush = heapq.heappush
    heapreplace = heapq.heapreplace

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]

    # scan all pairs
    for i in range(n - 1):
        xi, yi, zi = xs[i], ys[i], zs[i]
        for j in range(i + 1, n):
            dx = xi - xs[j]
            dy = yi - ys[j]
            dz = zi - zs[j]
            # using distance^2, to avoid square-root computations
            dist2 = dx*dx + dy*dy + dz*dz

            '''
            heapq is a min-heap, so we have quick access to the smallest element.
            However we need quick access to the largest element, to check the largest distance.
            To achieve this we negate the heap.
            '''
            if len(heap) < k:
                heappush(heap, (-dist2, i, j))
            else:
                if dist2 < -heap[0][0]:
                    heapreplace(heap, (-dist2, i, j))

    # convert back to positive dist2 and sort ascending
    out = [(-d2, i, j) for (d2, i, j) in heap]
    out.sort(key=lambda t: t[0])
    return out

def solve_part_1(path: str, k_connections: int = 1000) -> int:
    points = read_points(path)
    n = len(points)
    if n == 0:
        return 0

    edges = k_smallest_pairs(points, k_connections)

    dsu = DSU(n)
    for _, i, j in edges:
        dsu.union(i, j)

    comp_sizes = {}
    for i in range(n):
        r = dsu.find(i)
        comp_sizes[r] = comp_sizes.get(r, 0) + 1

    top_sizes = sorted(comp_sizes.values(), reverse=True)[:3]
    while len(top_sizes) < 3:
        top_sizes.append(1)

    return top_sizes[0] * top_sizes[1] * top_sizes[2]


'''
We are building a Minimum Spanning Tree (MST) using Prim's algorithm 
on the complete graph with squared Euclidean distance.
'''
def solve_part_2(path: str) -> int:
    points = read_points(path)
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
    print("Solution for part 1: ", solve_part_1("input.txt", k_connections=1000))
    print("Solution for part 2: ", solve_part_2("input.txt"))



