# Depth First Search (DFS)

def dfs(graph, node, visited):
    if node not in visited:
        print(node, end=" ")   # print current node
        visited.append(node)   # mark as visited

        # visit all neighbours recursively
        for neighbour in graph[node]:
            dfs(graph, neighbour, visited)


# Same graphs as your BFS program

graph1 = {
    1: [2,3],
    2: [4,5],
    3: [],
    4: [2,5],
    5: [2,4]
}

graph2 = {
    1: [2,7],
    2: [3,6],
    3: [4,5],
    4: [],
    5: [],
    6: [],
    7: [8,10],
    8: [9],
    9: [],
    10: []
}

graph3 = {
    1: [2,3],
    2: [5,6],
    3: [7,4],
    4: [8],
    5: [],
    6: [],
    7: [8],
    8: []
}

graph4 = {
    0: [1],
    1: [3],
    2: [1],
    3: [2,4],
    4: [5],
    5: [7],
    6: [4],
    7: [6]
}

print("DFS Traversal:")

visited = []
dfs(graph1, 1, visited)

print()
visited = []
dfs(graph2, 1, visited)

print()
visited = []
dfs(graph3, 1, visited)

print()
visited = []
dfs(graph4, 0, visited)
