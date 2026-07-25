def gbfs(graph, h, start, goal):

    open_list = [(start, [start], h[start])]
    visited = []

    while open_list:

        # choose node with smallest heuristic
        open_list.sort(key=lambda x: x[2])
        node, path, cost = open_list.pop(0)

        if node == goal:
            print("Path:", " -> ".join(path))
            print("Cost:", cost)
            print()
            return

        visited.append(node)

        for n in graph[node]:
            if n not in visited:
                open_list.append((n, path + [n], cost + h[n]))


# -------- Example 1 --------
print("Example 1")

graph1 = {
'A':['D','C','B'],
'D':['F'],
'C':['F','E'],
'B':['E'],
'E':['H'],
'H':['G'],
'F':['G'],
'G':[]
}

h1 = {'A':40,'B':32,'C':25,'D':35,'E':19,'F':17,'H':10,'G':0}

gbfs(graph1,h1,'A','G')


# -------- Example 2 --------
print("Example 2")

graph2 = {
'P':['R','C','A'],
'R':['E'],
'C':['U','M'],
'A':['M'],
'M':['L','U'],
'L':['N'],
'N':['S'],
'U':['S','N'],
'E':['S','U'],
'S':[]
}

h2 = {'P':10,'R':8,'C':6,'A':11,'M':9,'L':9,'U':4,'N':6,'E':3,'S':0}

gbfs(graph2,h2,'P','S')
