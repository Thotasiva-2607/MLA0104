def ucs(graph, start, goal):
    queue = [(start, 0)]   
    visited = []           

    while queue:

        
        min_index = 0
        for i in range(len(queue)):
            if queue[i][1] < queue[min_index][1]:
                min_index = i

        node, cost = queue.pop(min_index)  

        if node in visited:
            continue

        visited.append(node)   

        
        if node == goal:
            print("Minimum Cost to reach", goal, "is", cost)
            return

        
        for neighbour, weight in graph[node]:
            queue.append((neighbour, cost + weight))


graph1 = {
    'A': [('B', 3), ('C', 1)],
    'B': [('D', 3)],
    'C': [('D', 1), ('G',2)],
    'D': [('G', 3)],
    'S': [('A', 1), ('G', 12)],
    'G': []
}
graph2 = {
    'A': [('B', 2), ('C', 3), ('D', 4)],
    'B': [('E', 1), ('F',3)],
    'C': [('G',4)],
    'D': [('H', 2), ('I',1)],
    'E': [('J', 8), ('K', 4)],
    'F': [],
    'G': [('L', 5)],
    'H': [('M', 3)],
    'I': [],
    'J': [],
    'K': [],
    'L': [],
    'M': []
}
graph3 = {
    'V1': [('V2', 9), ('V3', 4)],
    'V2': [('V3', 2), ('V4', 7), ('V5', 3)],
    'V3': [('V4', 1), ('V5', 6)],
    'V4': [('V5', 4), ('V6', 8)],
    'V5': [('V6', 2)],
    'V6': []
}
graph4 = {
    'S': [('A', 3), ('B', 2),('C', 7)],
    'A': [('D', 3), ('E', 8),('G', 15)],
    'B': [('G', 20)],
    'C': [('G',6)],
    'D': [],
    'E': [],
    'G': []
}

ucs(graph1, 'S', 'G')
print()
ucs(graph2, 'A', 'M')
print()
ucs(graph3, 'V1', 'V6')
print()
ucs(graph4, 'S', 'G')
print()
