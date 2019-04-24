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
nodes_2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
node_network_2 = [[0, 4, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],  # 0
                  [4, 0, 2, inf, inf, inf, inf, inf, 2, inf, inf, inf, inf, inf, inf, inf, inf, inf, 1],
                  [inf, 2, 0, 7, inf, inf, inf, inf, inf, inf, inf, 5, inf, inf, inf, inf, inf, inf, inf],
                  [inf, inf, 7, 0, 3, 1, inf, inf, inf, 7, inf, inf, inf, inf, inf, inf, inf, inf, inf],
                  [inf, inf, inf, 3, 0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],
                  [inf, inf, inf, 1, inf, 0, inf, inf, inf, inf, 1, inf, inf, inf, inf, inf, inf, inf, inf],  # 5
                  [inf, inf, inf, inf, inf, inf, 0, 4, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 1],
                  [inf, inf, inf, inf, inf, inf, 4, 0, 3, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf],
                  [inf, 2, inf, inf, inf, inf, inf, 3, 0, inf, inf, 6, inf, inf, inf, inf, inf, inf, inf],
                  [inf, inf, inf, 7, inf, inf, inf, inf, inf, 0, inf, inf, 2, inf, inf, inf, inf, 4, inf],
                  [inf, inf, inf, inf, inf, 1, inf, inf, inf, inf, 0, inf, inf, 3, inf, inf, inf, 5, inf],  # 10
                  [inf, inf, 5, inf, inf, inf, inf, inf, 6, inf, inf, 0, inf, inf, 5, inf, inf, inf, inf],
                  [inf, inf, inf, inf, inf, inf, inf, inf, inf, 2, inf, inf, 0, inf, inf, 1, inf, inf, inf],
                  [inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 3, inf, inf, 0, inf, inf, inf, inf, inf],
                  [inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 5, inf, inf, 0, 2, inf, inf, inf],
                  [inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 1, inf, 2, 0, 6, inf, inf],  # 15
                  [inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 6, 0, inf, inf],
                  [inf, inf, inf, inf, inf, inf, inf, inf, inf, 4, 5, inf, inf, inf, inf, inf, inf, 0, inf],
                  [inf, 1, inf, inf, inf, inf, 1, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, 0]]

# pick test graph
nodes = nodes_2
node_network = node_network_2

dist, parent = sparse.csgraph.johnson(node_network, directed=False, return_predecessors=True)
mileage = 13
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
    constraint_sets[(start, end)] = []
    for start_node in range(len(all_paths[(start, end)])):
        # print(all_paths[(start, end)][start_node])
        distance_tracker = 0
        path_tracker = [all_paths[(start, end)][start_node]]
        over_counter = 0
        for node in range(start_node + 1, len(all_paths[(start, end)])):
            if all_distances[(start, end)][node - 1] + distance_tracker <= mileage:
                path_tracker.append(all_paths[(start, end)][node])
                distance_tracker += all_distances[(start, end)][node - 1]
            elif over_counter == 0:
                path_tracker.append(all_paths[(start, end)][node])
                distance_tracker += all_distances[(start, end)][node - 1]
                over_counter = 1
            elif over_counter == 1:
                break
        if distance_tracker >= mileage:
            constraint_sets[(start, end)].append(path_tracker[1:-1])
        # print(distance_tracker)
    print(constraint_sets[(start, end)])

# Uncomment if nodes should be output as letters
# constraint_sets_letters = constraint_sets.copy()
# for (start, end) in constraint_sets_letters.keys():
#     for n in range(len(constraint_sets_letters[start, end])):
#         constraint_sets_letters[start, end][n] = chr(constraint_sets[start, end][n] + 97)
#
# for (start, end) in constraint_sets_letters.keys():
#     print((chr(start + 97), chr(end + 97)), ":", constraint_sets_letters[(start, end)])

# Write to CSV file

max_length = 0
for (start, end) in constraint_sets.keys():
    for l in constraint_sets[(start, end)]:
        max_length = max(len(l), max_length)

header = []
for i in range(max_length):
    header.append('station_' + str(i + 1))

with open('ev_constraints.csv', mode='w', newline='') as ev_constraints:
    ev_writer = csv.writer(ev_constraints, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    ev_writer.writerow(header)
    for (start, end) in constraint_sets.keys():
        for l in constraint_sets[(start, end)]:
            if len(constraint_sets[(start, end)]) > 0:
                # print((start, end), ":", constraint_sets[(start, end)])
                ev_writer.writerow(l)