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

def solve_part_2(lines: list[str]) -> int:
    rows = [ln.rstrip("\n\r") for ln in lines]
    if not rows:
        return 0

    maxlen = max(len(r) for r in rows)
    rows = [r.ljust(maxlen) for r in rows]
    nrows = len(rows)

    is_sep = [all(rows[r][c] == " " for r in range(nrows)) for c in range(maxlen)]

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
        # Locate the operator as an anchor, then interpret only the region above it as digits.
        op_row = None
        op = None
        for r in range(nrows - 1, -1, -1):
            ops_here = [ch for ch in rows[r][start:end] if ch in "+*"]
            if ops_here:
                op_row = r
                op = ops_here[0]
                break

        if op_row is None or op is None:
            raise ValueError(f"Missing operator in block columns {start}:{end}")

        # Read numbers right-to-left to match the intended operand order in the layout.
        numbers = []
        for col in range(end - 1, start - 1, -1):
            digits = []
            for r in range(op_row):
                ch = rows[r][col]
                if ch.isdigit():
                    digits.append(ch)
            if digits:
                numbers.append(int("".join(digits)))

        if not numbers:
            raise ValueError(f"Missing numbers in block columns {start}:{end}")

        # Evaluate each block independently and accumulate the global result.
        total += sum(numbers) if op == "+" else math.prod(numbers)

    return total


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("Solution for part 1: ", solve_part_1(lines))
    print("Solution for part 2: ", solve_part_2(lines))

