# AI Search Algorithms

## 1. Depth First Search (DFS)

```text
DFS(Graph, StartNode)

    CREATE empty set Visited

    CALL DFS_Visit(StartNode)

DFS_Visit(Node)

    ADD Node to Visited
    VISIT Node

    FOR each Neighbor of Node in Graph DO
        IF Neighbor not in Visited THEN
            CALL DFS_Visit(Neighbor)
        END IF
    END FOR

END DFS_Visit
```

---

## 2. Breadth First Search (BFS)

```text
BFS(Graph, StartNode)

    CREATE empty queue Q
    CREATE empty set Visited

    ADD StartNode to Visited
    ENQUEUE StartNode into Q

    WHILE Q is not empty DO
        CurrentNode ← DEQUEUE Q
        VISIT CurrentNode

        FOR each Neighbor of CurrentNode in Graph DO
            IF Neighbor not in Visited THEN
                ADD Neighbor to Visited
                ENQUEUE Neighbor into Q
            END IF
        END FOR
    END WHILE

END BFS
```

---

## 3. Minimax Algorithm

```text
Minimax(Node, Depth, IsMax)

    IF Depth = 0 OR Node is leaf THEN
        RETURN value
    END IF

    IF IsMax THEN
        RETURN max(Minimax(children))
    ELSE
        RETURN min(Minimax(children))
    END IF

END Minimax
```

---

## 4. Alpha-Beta Pruning

```text
AlphaBeta(Node, Depth, α, β, IsMax)

    IF Depth = 0 THEN
        RETURN value
    END IF

    IF IsMax THEN
        FOR each Child DO
            α ← max(α, AlphaBeta(Child, Depth-1, α, β, FALSE))
            IF β ≤ α THEN
                BREAK
            END IF
        END FOR
        RETURN α

    ELSE
        FOR each Child DO
            β ← min(β, AlphaBeta(Child, Depth-1, α, β, TRUE))
            IF β ≤ α THEN
                BREAK
            END IF
        END FOR
        RETURN β
    END IF

END AlphaBeta
```

---

## 5. Uniform Cost Search (UCS)

```text
UniformCostSearch(Graph, Start, Goal)

    CREATE priority queue PQ
    CREATE set Visited

    INSERT (0, Start) into PQ

    WHILE PQ not empty DO

        (Cost, Node) ← REMOVE node with minimum cost

        IF Node = Goal THEN
            PRINT "Goal Reached with Cost", Cost
            EXIT
        END IF

        IF Node not in Visited THEN
            ADD Node to Visited

            FOR each Neighbor of Node DO
                INSERT (Cost + EdgeCost, Neighbor) into PQ
            END FOR
        END IF

    END WHILE

END UniformCostSearch
```

---

## 6. Greedy Best First Search (GBFS)

```text
GreedyBestFirstSearch(Graph, Start, Goal)

    CREATE priority queue PQ

    INSERT Start using heuristic value

    WHILE PQ not empty DO

        Node ← REMOVE node with lowest heuristic

        PRINT Node

        IF Node = Goal THEN
            EXIT
        END IF

        FOR each Neighbor of Node DO
            INSERT Neighbor into PQ
        END FOR

    END WHILE

END GreedyBestFirstSearch
```

---

## 7. A* Search

```text
AStar(Graph, Start, Goal)

    CREATE priority queue PQ

    INSERT (f = 0, Start)

    WHILE PQ not empty DO

        Node ← REMOVE node with lowest f

        IF Node = Goal THEN
            PRINT "Goal Reached"
            EXIT
        END IF

        FOR each Neighbor DO
            g ← path cost
            h ← heuristic
            f ← g + h

            INSERT Neighbor into PQ
        END FOR

    END WHILE

END AStar
```

---

## 8. Water Jug Problem

```text
WaterJug(Jug1, Jug2, Target)

    CREATE queue Q
    CREATE set Visited

    ENQUEUE (0,0)
    ADD (0,0) to Visited

    WHILE Q not empty DO

        (x,y) ← DEQUEUE Q

        IF x = Target OR y = Target THEN
            PRINT "Target Reached"
            EXIT
        END IF

        GENERATE possible states

        ADD unvisited states to Q

    END WHILE

    PRINT "Target Not Possible"

END WaterJug
```
