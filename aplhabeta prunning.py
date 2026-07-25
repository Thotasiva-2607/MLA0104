def alphabeta(depth, nodeIndex, maximizing, values, alpha, beta):

    # leaf node
    if depth == 3:
        return values[nodeIndex]

    if maximizing:
        best = -1000

        for i in range(2):
            val = alphabeta(depth+1, nodeIndex*2+i, False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)

            # pruning
            if beta <= alpha:
                break

        return best

    else:
        best = 1000

        for i in range(2):
            val = alphabeta(depth+1, nodeIndex*2+i, True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)

            # pruning
            if beta <= alpha:
                break

        return best


# leaf node values
values = [2,3,5,9,0,1,7,5]

result = alphabeta(0,0,True,values,-1000,1000)

print("Optimal value using Alpha-Beta Pruning:", result)
