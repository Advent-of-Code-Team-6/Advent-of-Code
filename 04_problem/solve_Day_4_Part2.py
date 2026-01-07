def solve_part2(filename):
    #open file
    try:
        with open(filename, 'r') as f:
            grid = [list(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{filename}' wurde nicht gefunden.")
        return 0

    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    total_removed = 0

    #Apply the rolls
    while True:
        to_remove = []
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    neighbor_rolls = 0
                    
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0: continue
                            
                            nr, nc = r + dy, c + dx
                            
                            if 0 <= nr < rows and 0 <= nc < cols:
                                if grid[nr][nc] == '@':
                                    neighbor_rolls += 1
                    if neighbor_rolls < 4:
                        to_remove.append((r, c))
        
        if not to_remove:
            break
            
        total_removed += len(to_remove)
        
        for r, c in to_remove:
            grid[r][c] = '.' 
            

    return total_removed

if __name__ == "__main__":
    dateiname = "input.txt"
    result = solve_part2(dateiname)
    print(f"Result: {result}")
