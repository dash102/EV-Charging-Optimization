from scipy import sparse

inf = float('inf')
node_network = [[0, inf, inf, 1, 3, 5, inf, inf],
                [inf, 0, 2, 5, inf, inf, inf, inf],
                [inf, 2, 0, inf, 4, inf, 7, 1],
                [1, 5, inf, 0, inf, inf, inf, inf],
                [3, inf, 4, inf, 0, 6, 3, inf],
                [5, inf, inf, inf, 6, 0, inf, inf],
                [inf, inf, 7, inf, 3, inf, 0, inf],
                [inf, inf, 1, inf, inf, inf, inf, 0]]

print(sparse.csgraph.johnson(node_network, directed=False))