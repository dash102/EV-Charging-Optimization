from scipy import sparse
import csv

inf = float('inf')

# first test graph
nodes_1 = [0, 1, 2, 3, 4, 5, 6, 7]  # nodes a through h
node_network_1 = [[0, inf, inf, 1, 3, 5, inf, inf],
                [inf, 0, 2, 5, inf, inf, inf, inf],
                [inf, 2, 0, inf, 4, inf, 7, 1],
                [1, 5, inf, 0, inf, inf, inf, inf],
                [3, inf, 4, inf, 0, 6, 3, inf],
                [5, inf, inf, inf, 6, 0, inf, inf],
                [inf, inf, 7, inf, 3, inf, 0, inf],
                [inf, inf, 1, inf, inf, inf, inf, 0]]

# second test graph
nodes_2 = []
node_network_2 = []

nodes = nodes_2
node_network = node_network_2

dist, parent = sparse.csgraph.johnson(node_network, directed=False, return_predecessors=True)
mileage = 8
all_paths = dict()
all_distances = dict()

for start_node in range(len(nodes)):
    for end_node in range(start_node + 1, len(nodes)):
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
            all_paths[(start_node, end_node)] = parent_nodes
            all_distances[(start_node, end_node)] = distances

# all_paths now stores entire path for each (start, end) pair
# all_distances similarly stores distances between each node in a path for each (start, end) pair

constraint_sets = dict()
for (start, end) in all_paths:
    single_constraint = []
    counter = 0
    for node in range(1, len(all_paths[(start, end)])):
        if counter + all_distances[(start, end)][node - 1] <= mileage:
            counter += all_distances[(start, end)][node - 1]
        else:
            single_constraint.append(all_paths[(start, end)][node - 1])
    constraint_sets[(start, end)] = single_constraint

constraint_sets_letters = constraint_sets.copy()
for (start, end) in constraint_sets_letters.keys():
    for n in range(len(constraint_sets_letters[start, end])):
        constraint_sets_letters[start, end][n] = chr(constraint_sets[start, end][n] + 97)

for (start, end) in constraint_sets_letters.keys():
    print((chr(start + 97), chr(end + 97)), ":", constraint_sets_letters[(start, end)])

# Write to CSV file

with open('ev_constraints.csv', mode='w', newline='') as ev_constraints:
    ev_writer = csv.writer(ev_constraints, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for (start, end) in constraint_sets.keys():
        if len(constraint_sets[(start, end)]) > 0:
            # print(constraint_sets[(start, end)])
            ev_writer.writerow(constraint_sets[(start, end)])