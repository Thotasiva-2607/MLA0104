jug1_capacity = 5
jug2_capacity = 3
target = 4

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def water_jug():

    
    if target > max(jug1_capacity, jug2_capacity) or target % gcd(jug1_capacity, jug2_capacity) != 0:
        print("No Solution Possible")
        return

    visited = []
    queue = [(0, 0)]   

    while queue:
        x, y = queue.pop(0)

        if (x, y) in visited:
            continue

        print("Current State:", (x, y))
        visited.append((x, y))

        
        if x == target or y == target:
            print("Target Achieved")
            return

        
        queue.append((jug1_capacity, y))

        
        queue.append((x, jug2_capacity))

       
        queue.append((0, y))

        
        queue.append((x, 0))

        
        transfer = min(x, jug2_capacity - y)
        queue.append((x - transfer, y + transfer))

        
        transfer = min(y, jug1_capacity - x)
        queue.append((x + transfer, y - transfer))
water_jug()
