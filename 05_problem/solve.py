# Converting the input.txt from 
# ranges seperated by newlines, i.e. 123-987\n ...
# and (seperated by an empty line)
# numbers seperated by newlines, i.e. 234\n ...
# to a list of tuples, i.e. ranges = [(123,987),...], and list of numbers, i.e. numbers = [234,...]

input_text = open('input.txt').read()

def parse_input(input_text):
    # Convert text file lines into list of strings
    lines = input_text.strip().split('\n')

    # Find empty 'line' that separates ranges from numbers
    separator_index = lines.index('')
    
    # Parse ranges section into list of tuples
    ranges = []
    for line in lines[:separator_index]:
        start, end = line.split('-')
        ranges.append((int(start), int(end)))
    
    # Parse numbers section into list
    numbers = []
    for line in lines[separator_index + 1:]:
        numbers.append(int(line))
    
    return ranges, numbers

ranges, numbers = parse_input(input_text)


# Merge overlapping or consecutive ranges
# i.e. 11-14 with 15-20, or 22-25 with 23-30
def merge_ranges(ranges):

    # Sort ranges by starting point
    ranges.sort(key=lambda x: x[0])
    
    mergedRanges = []

    # Current range being built
    i = 0
    # Range being compared
    j = 1

    current_start = ranges[i][0]
    current_end = ranges[i][1]
    
    while j < len(ranges):
        comp_start = ranges[j][0]
        comp_end = ranges[j][1]
        
        # Check if ranges overlap or are consecutive
        if current_end >= comp_start - 1:
            # If ranges merge, then extend current range to include both
            current_end = max(current_end, comp_end)
            j += 1
        else:
            # If ranges don't merge, then save current and start new range
            mergedRanges.append((current_start, current_end))
            i = j
            j = j + 1
            current_start = ranges[i][0]
            current_end = ranges[i][1]
    
    # Add the final range
    mergedRanges.append((current_start, current_end))
    
    return mergedRanges


 # Count how many numbers fall within the merged ranges
def count_numbers_in_ranges(numbers, ranges):

    if not ranges:
        return 0
    
    count = 0
    first_start = ranges[0][0]
    last_end = ranges[-1][1]
    
    for num in numbers:
        # Skip numbers outside of all ranges (for optimization)
        if num < first_start or num > last_end:
            continue
        
        # Check if number falls within any range
        for start, end in ranges:
            if num <= end:
                if num >= start:
                    count += 1
                # When match found, break, move to next number
                break
    
    return count

#########
# Part 1: Count how many fresh ingredients there are
#########
print("The answer for Part 1 is: ", count_numbers_in_ranges(numbers, merge_ranges(ranges)))

#########
# Part 2: Count how many total ingredients are considered fresh
#########
mergedRanges = merge_ranges(ranges)
freshIngredientCount = 0

# Sum up the size of each merged range
# Range size = (end - start + 1) because ranges are inclusive
# (i.e. 12 - 10 = 2, but 10,11,12 are 3 numbers)
for mR in mergedRanges:
    freshIngredientCount += (mR[1] - mR[0] + 1)

print("The answer for Part 2 is: ", freshIngredientCount)
