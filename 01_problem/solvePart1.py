def solve_safe(filename):
    # The pointer starts at 50
    current_pos = 50
    zero_count = 0
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                rotation = line.strip()
                
                # First character is the direction (L/R)
                direction = rotation[0]
                
                # The rest is the number
                try:
                    amount = int(rotation[1:])
                except ValueError:
                    continue  # Skip if conversion fails
                
                if direction == 'R':
                    # Right rotation: Add
                    current_pos = (current_pos + amount) % 100
                elif direction == 'L':
                    # Left rotation: Subtract
                    current_pos = (current_pos - amount) % 100
                    
                # Check if we landed on 0
                if current_pos == 0:
                    zero_count += 1
                    
        return zero_count

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return 0

#Main
if __name__ == "__main__":
    result = solve_safe('input.txt')
    print(f"The pointer landed on zero {result} times.")