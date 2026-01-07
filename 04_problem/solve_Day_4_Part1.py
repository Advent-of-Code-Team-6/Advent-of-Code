def count_accessible_rolls(filename):
    #Read File
    try:
        with open(filename, 'r') as f:
            grid = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File dose not exit")
        return 0

    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    accessible_count = 0

    #check is removable
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                neighbor_rolls = 0
                
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        
                        nr, nc = r + dy, c + dx
                        
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr][nc] == '@':
                                neighbor_rolls += 1
                
                if neighbor_rolls < 4:
                    accessible_count += 1

    return accessible_count


if __name__ == "__main__":
    result = count_accessible_rolls("input.txt")
    print(f"Result: {result}")