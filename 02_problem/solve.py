# Converting the input.txt from ranges seperated by commas, i.e. 123-987,...
# to a list of tuples, i.e. ranges = [(123,987),...]

with open('input.txt', 'r') as f:
    input = f.read().strip()

ranges = [tuple(map(int, r.split('-'))) for r in input.split(',')]

# re is the 'Regular Expression Operations' library
import re

# Creating a RegEx pattern for identifying numbers with repeating digit sequences
# r'...' = raw string (to avoid issues with '\')
# (\d+) = capture one or more digits
# ^...$ = ensure entire number is repeated pattern (i.e. avoiding a match for 100, where 0 repeats in the end)

# \1 = match already captured digits (sequence) once more --- [FOR PART 1]
pattern_pt1 = r'^(\d+)\1$'

# \1+ = match already captured digits (sequence) one OR MORE times --- [FOR PART 2]
pattern_pt2 = r'^(\d+)\1+$'

# Initialising invalid ID sums for Part 1 and 2
invalid_sum_pt1 = 0
invalid_sum_pt2 = 0

# Loop through each ID in the ranges
# Validate them against the RegEx patterns
# Add invalid IDs to the total sum
for start, end in ranges:
    for id_num in range(start, end + 1):
        if re.search(pattern_pt1, str(id_num)):
            invalid_sum_pt1 += id_num
        if re.search(pattern_pt2, str(id_num)):
            invalid_sum_pt2 += id_num

print("The answer for Part 1 is: ", invalid_sum_pt1)
print("The answer for Part 2 is: ", invalid_sum_pt2)
