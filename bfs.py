def bfs(graph, start):
    visited = []          
    queue = []             

    visited.append(start) 
    queue.append(start)   

    while queue:
        node = queue.pop(0)   
        print(node, end=" ")  

        
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.append(neighbour)  
                queue.append(neighbour)    


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

print("BFS Traversal:")
bfs(graph1, 1)
print()
bfs(graph2, 1)
print()
bfs(graph3, 1)
print()
bfs(graph4, 0)
