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

if __name__ == "__main__":
    # Keep I/O separate from logic so functions remain testable.
    grid = read_grid("input.txt")
    print(solve_part_1(grid))

