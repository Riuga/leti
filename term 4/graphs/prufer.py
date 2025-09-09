import sys


def prufer_to_tree(n, code):
    if (n == 0):
        return [('', '')]

    degree = [1] * (n + 2)
    for num in code:
        degree[num] += 1

    leaves = []
    for i in range(0, n + 2):
        if degree[i] == 1:
            leaves.append(i)

    edges = []
    for num in code:
        leaf = min(leaves)
        edges.append((min(leaf, num), max(leaf, num)))
        degree[leaf] -= 1
        degree[num] -= 1
        leaves.remove(leaf)
        if degree[num] == 1:
            leaves.append(num)
    edges.append((min(leaves), max(leaves)))
    return edges


input_data = sys.stdin.read().strip().splitlines()
n = int(input_data[0])
code = []
if (n != 0):
    code = list(map(int, input_data[1].split()))

edges = prufer_to_tree(n, code)

for edge in edges:
    print(edge[0], edge[1])
