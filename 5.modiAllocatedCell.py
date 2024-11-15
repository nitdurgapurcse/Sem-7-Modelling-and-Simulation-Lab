import numpy as np
import sys

def check_balanced(demand, supply):
    total_demand = np.sum(demand)
    total_supply = np.sum(supply)
    if total_demand == total_supply:
        print("The problem is balanced.")
        print("Total supply = Total demand =", total_supply)
        return True
    else:
        print("The problem is not balanced.")
        print("Total supply =", total_supply)
        print("Total demand =", total_demand)
        return False

def get_uv(allocation, cost):
    m, n = allocation.shape
    u = np.full((m,), np.inf)
    v = np.full((n,), np.inf)
    u[0] = 0
    i, j = 0, 0
    while np.any(u == np.inf) or np.any(v == np.inf):
        if allocation[i][j] != 0:
            if u[i] != np.inf and v[j] == np.inf:
                v[j] = cost[i][j] - u[i]
            elif v[j] != np.inf and u[i] == np.inf:
                u[i] = cost[i][j] - v[j]
        if i == m - 1 and j == n - 1:
            i, j = 0, 0
        elif j == n - 1:
            i, j = i + 1, 0
        else:
            j += 1
    return u, v

def get_delta(cost, allocation, u, v):
    m, n = cost.shape
    delta = np.zeros((m, n))
    check1 = check2 = check = 1
    for i in range(m):
        for j in range(n):
            if allocation[i][j] == 0:
                delta[i][j] = cost[i][j] - (u[i] + v[j])
                if delta[i][j] < 0:
                    check1 = -1
                if delta[i][j] == 0:
                    check2 = 0
    if check1 == -1:
        check = -1
    elif check2 == 0:
        check = 0
    return delta, check

def get_next_nodes(loop, unvisited):
    last_node = loop[-1]
    second_last_node = loop[-2] if len(loop) >= 2 else None
    nodes_same_row = [n for n in unvisited if n[0] == last_node[0]]
    nodes_same_col = [n for n in unvisited if n[1] == last_node[1]]
    if second_last_node is None:
        return nodes_same_row + nodes_same_col
    move_was_in_row = second_last_node[0] == last_node[0]
    return nodes_same_col if move_was_in_row else nodes_same_row

def find_valid_loop(allocated_nodes, starting_node):
    def recursive2(current_loop):
        if len(current_loop) > 3:
            ways_closed = len(get_next_nodes(current_loop, [starting_node]))
            if ways_closed == 1:
                return current_loop
        unvisited = list(set(allocated_nodes) - set(current_loop))
        next_nodes = get_next_nodes(current_loop, unvisited)
        for next_node in next_nodes:
            new_loop = recursive2(current_loop + [next_node])
            if new_loop:
                return new_loop
        return None
    return recursive2([starting_node])

def get_new_allocations(allocated_nodes, loop):
    even_positions = loop[0::2]
    odd_positions = loop[1::2]
    def get_value(position):
        return next(value for pos, value in allocated_nodes if pos == position)
    leaving_position = min(odd_positions, key=get_value)
    leaving_value = get_value(leaving_position)
    new_allocations = []
    for pos, value in [(pos, value) for pos, value in allocated_nodes if pos != leaving_position] + [(loop[0], 0)]:
        if pos in even_positions:
            value += leaving_value
        elif pos in odd_positions:
            value -= leaving_value
        new_allocations.append((pos, value))
    return new_allocations

def recursive1(cost, allocation):
    u, v = get_uv(allocation, cost)
    delta, check = get_delta(cost, allocation, u, v)
    print("\nu: ", u)
    print("v: ", v)
    print("delta:\n", delta)
    if check == 1 or check == 0:
        if check == 1:
            print("This is an optimal solution.")
        else:
            print("This is an optimal solution but there exist alternate solutions.")
        print("Optimal Allocation Matrix:\n", allocation)
        optimal_total_cost = sum(cost[i][j] * allocation[i][j] for i in range(cost.shape[0]) for j in range(cost.shape[1]))
        print("Optimal total transportation cost using MODI Method:", optimal_total_cost)
    else:
        print("This is not an optimal solution.\n")
        min_delta = np.min(delta)
        min_delta_indices = np.argwhere(delta == min_delta)
        a, b = min_delta_indices[0]
        allocated_nodes = [((i, j), allocation[i][j]) for i in range(cost.shape[0]) for j in range(cost.shape[1]) if allocation[i][j] != 0]
        loop = find_valid_loop([x for x, y in allocated_nodes], (a, b))
        temp = get_new_allocations(allocated_nodes, loop)
        new_allocations = np.zeros_like(allocation)
        for x, y in temp:
            new_allocations[x[0]][x[1]] = y
        print("New allocation matrix:\n", new_allocations)
        recursive1(cost, new_allocations)

if __name__ == '__main__':
    m = int(input("Enter the number of storage houses: "))
    n = int(input("Enter the number of showrooms: "))
    cost = np.zeros((m, n))
    supply = np.zeros((m,))
    demand = np.zeros((n,))
    allocation = np.zeros((m, n))

    print("\nEnter the daily supply capacities of the houses in order:")
    for i in range(m):
        supply[i] = int(input())

    print("\nEnter the daily demand of the showrooms in order:")
    for j in range(n):
        demand[j] = int(input())

    if not check_balanced(demand, supply):
        sys.exit(1)

    for i in range(m):
        print("\nEnter the transportation cost between house", i + 1, "to the showrooms in order:")
        for j in range(n):
            cost[i][j] = int(input())

    total_cost = 0
    no_alloc = 0
    for i in range(m):
        print("\nEnter the allocated units for house", i + 1, "to the showrooms in order:")
        for j in range(n):
            allocation[i][j] = int(input())
            if allocation[i][j] != 0:
                total_cost += cost[i][j] * allocation[i][j]
                no_alloc += 1

    print("Allocation matrix:\n", allocation)
    print("Initial basic feasible solution cost:", total_cost)

    if no_alloc == m + n - 1:
        print("The solution is non-degenerate as the number of allocations =", no_alloc)
        recursive1(cost, allocation)
    else:
        print("The solution is degenerate.")
        print("Number of allocations =", no_alloc)
        print("m + n - 1 =", m + n - 1)

'''
Enter the number of storage houses: 3
Enter the number of showrooms: 4

Enter the daily supply capacities of the houses in order:
30
40
53

Enter the daily demand of the showrooms in order:
22
35
25
41
The problem is balanced.
Total supply = Total demand = 123.0

Enter the transportation cost between house 1 to the showrooms in order:
23
27
16
18

Enter the transportation cost between house 2 to the showrooms in order:
12
17
28
51

Enter the transportation cost between house 3 to the showrooms in order:
22
28
12
32

Enter the allocated units for house 1 to the showrooms in order:
0
0
0
11

Enter the allocated units for house 2 to the showrooms in order:
6
3
0
4

Enter the allocated units for house 3 to the showrooms in order:
0
7
12
0
Allocation matrix:
 [[ 0.  0.  0. 11.]
 [ 6.  3.  0.  4.]
 [ 0.  7. 12.  0.]]
Initial basic feasible solution cost: 865.0
The solution is non-degenerate as the number of allocations = 6

u:  [ 0. 33. 44.]
v:  [-21. -16. -32.  18.]
delta:
 [[ 44.  43.  48.   0.]
 [  0.   0.  27.   0.]
 [ -1.   0.   0. -30.]]
This is not an optimal solution.

New allocation matrix:
 [[ 0.  0.  0. 11.]
 [ 6.  7.  0.  0.]
 [ 0.  3. 12.  4.]]

u:  [ 0.  3. 14.]
v:  [ 9. 14. -2. 18.]
delta:
 [[14. 13. 18.  0.]
 [ 0.  0. 27. 30.]
 [-1.  0.  0.  0.]]
This is not an optimal solution.

New allocation matrix:
 [[ 0.  0.  0. 11.]
 [ 3. 10.  0.  0.]
 [ 3.  0. 12.  4.]]

u:  [ 0.  4. 14.]
v:  [ 8. 13. -2. 18.]
delta:
 [[15. 14. 18.  0.]
 [ 0.  0. 26. 29.]
 [ 0.  1.  0.  0.]]
This is an optimal solution.
Optimal Allocation Matrix:
 [[ 0.  0.  0. 11.]
 [ 3. 10.  0.  0.]
 [ 3.  0. 12.  4.]]
Optimal total transportation cost using MODI Method: 742.0
'''