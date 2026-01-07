def solve_batteries_part2(input_data):
    total_joltage = 0
    
    lines = input_data.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Wir brauchen exakt 12 Stellen
        needed_length = 12
        
        # Wenn die Zeile kürzer als 12 ist, geht es nicht (sollte im Puzzle nicht passieren)
        if len(line) < needed_length:
            continue

        result_digits = []
        current_pos = 0
        digits_to_find = needed_length
        
        # Wir suchen 12 mal hintereinander die beste Ziffer
        for i in range(needed_length):
            # Wie viele Ziffern müssen wir NACH der aktuellen noch finden?
            remaining_needed = digits_to_find - 1
            
            # Das Ende des Suchfensters:
            # Wir müssen am Ende des Strings genug Platz lassen für den Rest.
            # Beispiel: String-Länge 20. Wir brauchen noch 11 Ziffern nach dieser.
            # Dann darf unser Suchfenster nur bis Index (20 - 11) gehen.
            search_end = len(line) - remaining_needed
            
            # Das Fenster ausschneiden, in dem wir suchen dürfen
            window = line[current_pos : search_end]
            
            # Die höchste Ziffer in diesem Fenster finden ('9' ist besser als '8' etc.)
            # Wir nehmen das erste Vorkommen der höchsten Ziffer, um möglichst viel
            # "Platz" rechts davon übrig zu behalten (auch wenn das für den Wert egal ist).
            best_digit = '0'
            best_relative_index = -1
            
            for idx, char in enumerate(window):
                if char == '9': # Optimierung: Besser als 9 geht nicht
                    best_digit = char
                    best_relative_index = idx
                    break
                if char > best_digit:
                    best_digit = char
                    best_relative_index = idx
            
            # Ziffer zum Ergebnis hinzufügen
            result_digits.append(best_digit)
            
            # Neue Startposition für die nächste Runde:
            # Rechts neben der gerade gefundenen Ziffer
            current_pos += best_relative_index + 1
            
            # Ein Ziffer weniger zu finden
            digits_to_find -= 1
            
        # Die 12 Ziffern zu einer Zahl zusammenfügen und addieren
        num_str = "".join(result_digits)
        total_joltage += int(num_str)

    return total_joltage


def read_input_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
            return content
    except FileNotFoundError:
        print(f"File dose not exist")
        return 0

mein_input = read_input_file(filename='input.txt')

ergebnis = solve_batteries_part2(mein_input)
print("------------------------------------------------")
print(f"NEUE GESAMT-JOLTAGE (TEIL 2): {ergebnis}")
print("------------------------------------------------")
