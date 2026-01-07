from collections import deque

def read_grid(path: str) -> list[list[str]]:
    # Simple parser variant kept for compatibility with uneven row lengths.
    grid = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n\r")
            if line == "":
                continue
            grid.append(list(line))
    return grid

def solve_part_1(grid: list[list[str]]) -> int:
    H = len(grid)
    if H == 0:
        return 0
    W = len(grid[0])

    # Use 'S' as a unique start anchor to avoid hard-coding coordinates.
    sr = sc = None
    for r in range(H):
        for c in range(W):
            if grid[r][c] == "S":
                sr, sc = r, c
                break
        if sr is not None:
            break
    if sr is None:
        raise ValueError("No 'S' found in grid")

    # Model splitting as a queue of independent beam fronts.
    q = deque([(sr + 1, sc)])
    visited = set()  # Prevent re-processing already-resolved paths.
    splits = 0

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < H and 0 <= c < W

    while q:
        r, c = q.popleft()
        if not in_bounds(r, c):
            continue

        # Advance straight down until either a splitter is hit or the path is known.
        while in_bounds(r, c):
            if (r, c) in visited:
                break
            visited.add((r, c))

            if grid[r][c] == "^":
                splits += 1
                # A splitter creates two independent continuations at the same row.
                q.append((r, c - 1))
                q.append((r, c + 1))
                break

            r += 1

    return splits

def solve_part_2(grid: list[list[str]]) -> int:
    H = len(grid)
    if H == 0:
        return 0

    # Use 'S' as the single source of the initial state.
    sr = sc = None
    for r in range(H):
        for c, ch in enumerate(grid[r]):
            if ch == "S":
                sr, sc = r, c
                break
        if sr is not None:
            break
    if sr is None:
        raise ValueError("No 'S' found in grid")

    def in_bounds(r: int, c: int) -> bool:
        # Support ragged grids by checking row-specific width.
        return 0 <= r < H and 0 <= c < len(grid[r])

    # Precompute the next splitter per cell to avoid repeated downward scans.
    next_split = [[None] * len(grid[r]) for r in range(H)]

    # Bottom-up fill lets each cell reuse the information from the cell below.
    for r in range(H - 1, -1, -1):
        for c in range(len(grid[r])):
            if grid[r][c] == "^":
                next_split[r][c] = r
            else:
                if r + 1 < H and c < len(grid[r + 1]):
                    next_split[r][c] = next_split[r + 1][c]
                else:
                    next_split[r][c] = None

    memo = {}
    visiting = set()  # Defensive cycle detection to avoid infinite recursion on invalid inputs.

    def ways(r: int, c: int) -> int:
        # Leaving the grid corresponds to one completed timeline.
        if not in_bounds(r, c):
            return 1

        key = (r, c)
        if key in memo:
            return memo[key]

        if key in visiting:
            raise ValueError("Cycle detected (would create infinite timelines).")

        visiting.add(key)

        s = next_split[r][c]
        if s is None:
            ans = 1
        else:
            ans = ways(s, c - 1) + ways(s, c + 1)

        visiting.remove(key)
        memo[key] = ans
        return ans

    # Start immediately below 'S' to match the puzzle's initial beam direction.
    return ways(sr + 1, sc)

if __name__ == "__main__":
    # Keep I/O separate from logic so functions remain testable.
    grid = read_grid("input.txt")
    print(solve_part_1(grid))
    print(solve_part_2(grid))

