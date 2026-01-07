def solve_safe_part2(filename):
    # The pointer starts at 50
    current_pos = 50
    zero_hits = 0
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                rotation = line.strip()
                
                # First character is the direction (L/R)
                direction = rotation[0]

                try:
                    amount = int(rotation[1:])
                except ValueError:
                    # Skip invalid lines
                    continue
                    
                if direction == 'R':
                    target_pos = current_pos + amount
                    
                    # Calculate how often a full circle occurs
                    hits = (target_pos // 100) - (current_pos // 100)
                    zero_hits += hits
                    
                    # Update current position
                    current_pos = target_pos % 100
                    
                elif direction == 'L':
                    target_pos = current_pos - amount

                    # Calculate how often a full circle occurs
                    hits = ((current_pos - 1) // 100) - ((target_pos - 1) // 100)
                    zero_hits += hits
                    
                    # Update current position
                    current_pos = target_pos % 100

        return zero_hits

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return 0

#Main
if __name__ == "__main__":
    ergebnis = solve_safe_part2('input.txt')
    print(f"SOLUTION PART 2: {ergebnis}")