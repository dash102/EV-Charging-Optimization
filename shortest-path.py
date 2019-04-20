from scipy import sparse

inf = float('inf')
nodes = [0, 1, 2, 3, 4, 5, 6, 7]  # nodes a through h
node_network = [[0, inf, inf, 1, 3, 5, inf, inf],
                [inf, 0, 2, 5, inf, inf, inf, inf],
                [inf, 2, 0, inf, 4, inf, 7, 1],
                [1, 5, inf, 0, inf, inf, inf, inf],
                [3, inf, 4, inf, 0, 6, 3, inf],
                [5, inf, inf, inf, 6, 0, inf, inf],
                [inf, inf, 7, inf, 3, inf, 0, inf],
                [inf, inf, 1, inf, inf, inf, inf, 0]]

dist, parent = sparse.csgraph.johnson(node_network, directed=False, return_predecessors=True)
print(dist)
print(parent)

mileage = 7
constraint_node = []
constraint_distance = []

for start_node in range(len(nodes)):
    for end_node in range(start_node + 1, len(nodes)):
        if start_node == 0 and end_node == 7:
            # print(start_node, end_node)
            parent_nodes = [end_node]
            distances = []
            curr_node = end_node
            while parent[start_node][parent_nodes[-1]] != -9999:
                curr_node = parent[start_node][parent_nodes[-1]]
                distances.append(dist[curr_node][parent_nodes[-1]])
                # print(start_node, parent_node[-1])
                parent_nodes.append(parent[start_node][parent_nodes[-1]])
            parent_nodes.reverse()
            distances.reverse()

            sub_constraint = []
            sub_distance_constraint = []

            distance_tracker = 0
            last_distance = 0
