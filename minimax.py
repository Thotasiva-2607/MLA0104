def minimax(depth, nodeIndex, isMax, values):

    # if leaf node
    if depth == 3:
        return values[nodeIndex]

    if isMax:
        return max(
            minimax(depth+1, nodeIndex*2, False, values),
            minimax(depth+1, nodeIndex*2+1, False, values)
        )

    else:
        return min(
            minimax(depth+1, nodeIndex*2, True, values),
            minimax(depth+1, nodeIndex*2+1, True, values)
        )


# leaf node values from the tree
values = [2,3,5,9,0,1,7,5]

result = minimax(0,0,True,values)

print("Optimal value using Mini-Max:", result)
