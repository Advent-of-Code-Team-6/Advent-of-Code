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

    max_pairs = n * (n - 1) // 2
    k = min(k_connections, max_pairs)

    edges = k_smallest_pairs(points, k)

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

if __name__ == "__main__":
    print(solve_part_1("input.txt", k_connections=1000))
