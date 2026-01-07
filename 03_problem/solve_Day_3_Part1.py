def solve_batteries(input_data):
    total_joltage = 0
    lines = input_data.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        digits = [int(c) for c in line if c.isdigit()]
        
        current_max = 0
        

        for i in range(len(digits)):
            for j in range(i + 1, len(digits)):
                
                val = digits[i] * 10 + digits[j]
                if val > current_max:
                    current_max = val
        
        total_joltage += current_max

    return total_joltage

def read_input_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
            return solve_batteries(content)
    except FileNotFoundError:
        print(f"File dose not exist")
        return 0

if __name__ == "__main__":
    dateiname = 'input.txt'
    result = read_input_file(dateiname)
    print(f"Solution: {result}")