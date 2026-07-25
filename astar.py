def astar(graph, h, start, goal):

    open_list = [(start, 0, [start])]   # (node, g_cost, path)
    closed = []

    while open_list:

        # choose node with lowest f(n)=g+h
        open_list.sort(key=lambda x: x[1] + h[x[0]])
        node, g, path = open_list.pop(0)

        if node == goal:
            print("Path:", " -> ".join(path))
            print("Cost:", g)
            print()
            return

        closed.append(node)

        for n, cost in graph[node]:
            if n not in closed:
                open_list.append((n, g + cost, path + [n]))


# -------- Example 1 --------
print("Example 1")

graph1 = {
'S':[('A',3),('D',4)],
'A':[('B',4),('D',5)],
'B':[('C',4),('E',5)],
'C':[],
'D':[('E',2)],
'E':[('F',4)],
'F':[('G',3.5)],
'G':[]
}

h1 = {'S':11.5,'A':10.1,'B':5.8,'C':3.4,'D':9.2,'E':7.1,'F':3.5,'G':0}

astar(graph1, h1, 'S', 'G')


# -------- Example 2 --------
print("Example 2")

graph2 = {
'A':[('B',1),('C',4)],
'B':[('D',3),('C',2)],
'C':[('E',5)],
'D':[('F',2),('G',4)],
'E':[('G',3)],
'F':[('G',1)],
'G':[]
}

h2 = {'A':5,'B':6,'C':4,'D':3,'E':3,'F':1,'G':0}

astar(graph2, h2, 'A', 'G')


# -------- Example 3 --------
print("Example 3")

graph3 = {
'S':[('A',3),('D',2)],
'A':[('B',5),('C',10)],
'B':[('C',2),('E',1)],
'C':[('G',4)],
'D':[('B',1),('E',4)],
'E':[('G',3)],
'G':[]
}

h3 = {'S':7,'A':9,'B':4,'C':2,'D':5,'E':3,'G':0}

astar(graph3, h3, 'S', 'G')
