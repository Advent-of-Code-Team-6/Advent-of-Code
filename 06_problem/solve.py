import math

def solve_part_1(lines: list[str]) -> int:
    rows = [ln.rstrip("\n\r") for ln in lines]
    if not rows:
        return 0

    maxlen = max(len(r) for r in rows)
    rows = [r.ljust(maxlen) for r in rows]

    # Identify fully blank columns to split independent expression blocks.
    is_sep = [all(rows[r][c] == " " for r in range(len(rows))) for c in range(maxlen)]

    # Group contiguous non-separator columns into blocks.
    blocks = []
    c = 0
    while c < maxlen:
        while c < maxlen and is_sep[c]:
            c += 1
        if c >= maxlen:
            break
        start = c
        while c < maxlen and not is_sep[c]:
            c += 1
        blocks.append((start, c))

    total = 0

    for start, end in blocks:
        nums = []
        op = None

        # Treat each block as a self-contained expression (operator + operands).
        for r in rows:
            token = r[start:end].strip()
            if not token:
                continue
            if token in {"+", "*"}:
                op = token
            else:
                nums.append(int(token))

        if op is None:
            raise ValueError(f"Missing operator (+ or *) in block columns {start}:{end}")
        if not nums:
            raise ValueError(f"Missing numbers in block columns {start}:{end}")

        # Use built-ins to keep evaluation fast and clear for variable operand counts.
        total += sum(nums) if op == "+" else math.prod(nums)

    return total


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("Solution for part 1: ", solve_part_1(lines))

