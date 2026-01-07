# First, we parse the input file to create a graph
# Turning "aaa: you hhh\n ..."
# Into "graph = {'aaa' : ['you', 'hhh'], ...}"

def parse_input(filename):
    graph = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            device, outputs = line.split(': ')
            graph[device] = outputs.split()
    
    return graph

"""
1. Initially considered tree structure, putting "you" as the root, constructing the paths,
then checking which paths end in leafs marked "out.
2. Realised the redundancy of data in such a tree (since a node can have multiple incoming edges),
and that a graph is much more fitting.
3. The text mentions "Data only ever flows from a device through its outputs; it can't flow backwards",
Thus we can assume that there will be no cycles, and we don't need aditional logic to handle endless loops.
And the flow has a direction.

==> We have a Directed Acyclical Graph.
"""

# Recursive algorithm which performs a Depth-First Search of the graph
def count_paths(graph, current_node):
    # Each complete path, which ends in 'out', returns 1
    if current_node == "out":
        return 1
    
    # Each complete path, which does not end in 'out', returns 0
    if current_node not in graph:
        return 0
    
    # Sum paths found through each neighbor
    total = 0
    for neighbor in graph[current_node]:
        total += count_paths(graph, neighbor)
    
    # Return total number of paths from this node to 'out'
    return total


"""
In part 1 we had the idea that you could make the algorithm more effective by saving paths, 
which you already went through. 
Thus knowing if you ended up at 'out' without re-checking the full path.

i.e. [aaa -> bbb -> fff -> out] is cached,
so in case of [you -> ddd -> aaa], we already know this ends in 'out'.

Turns out this process is called "Memoization".
The naive approach of the part 2 algorithm was running forever.
After implementing memoization, it became clear why:
There were trillions of paths (needing trillions of calculations) which fulfill the dac/fft requirement.
"""

# We enhance the original algorithm with booleans for visiting dac & fft
# Additionally, we introduce memoization
def count_paths_with_requirements(graph, current_node, dac_visited, fft_visited, memo=None):
    # Initialize memoization cache on first call
    if memo is None:
        memo = {}
    
    # Check if we've already calculated this state
    state = (current_node, dac_visited, fft_visited)
    if state in memo:
        return memo[state]
    
    # Update visited booleans if we're at a required node
    if current_node == "dac":
        dac_visited = True
    if current_node == "fft":
        fft_visited = True
    
    # Reached 'out', but we count it only if both requirements were met
    if current_node == "out":
        result = 1 if (dac_visited and fft_visited) else 0
        memo[state] = result
        return result
    
    # Dead end
    if current_node not in graph:
        memo[state] = 0
        return 0
    
    # Sum paths found through each neighbor
    total = 0
    for neighbor in graph[current_node]:
        total += count_paths_with_requirements(graph, neighbor, dac_visited, fft_visited, memo)

    # Cache result before returning
    memo[state] = total
    return total


# Main execution
graph = parse_input('input11.txt')

result_pt1 = count_paths(graph, 'you')
result_pt2 = count_paths_with_requirements(graph, 'svr', False, False)

print("Number of paths from 'you' to 'out': ", result_pt1)
print("Number of paths from 'svr' to 'out' visiting both 'dac' and 'fft': ", result_pt2)