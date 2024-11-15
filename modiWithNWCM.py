import numpy as np
from tabulate import tabulate

def north_west_corner_rule(supply, demand, costs):
    num_rows = len(supply)
    num_cols = len(demand)
    allocation_matrix = [[0] * num_cols for _ in range(num_rows)]
    bfs = []
    total_cost = 0
    i, j = 0, 0

    # North West Corner Rule allocation
    while i < num_rows and j < num_cols:
        # Allocate the minimum of supply or demand
        allocation = min(supply[i], demand[j])
        allocation_matrix[i][j] = allocation
        bfs.append(((i, j), allocation))
        current_cost = allocation * costs[i][j]
        total_cost += current_cost

        # Adjust supply and demand after allocation
        supply[i] -= allocation
        demand[j] -= allocation

        # Move to the next cell based on remaining supply and demand
        if supply[i] == 0:
            i += 1
        elif demand[j] == 0:
            j += 1

    # Display the allocation matrix
    print("\nAllocation Matrix:")
    headers = [f'Demand {i+1}' for i in range(num_cols)]
    print(tabulate(allocation_matrix, headers, tablefmt="grid", colalign=("center",) * num_cols))
    print(f"\nTotal Transportation Cost (Initial Basic Feasible Solution) using NWCR: {total_cost}")
    return bfs

def modi_method(costs, supply, demand):
    # Calculate the initial BFS using the NWCR method
    balanced_supply, balanced_demand, balanced_costs = get_balanced(supply, demand, costs)
    bfs = north_west_corner_rule(balanced_supply.copy(), balanced_demand.copy(), balanced_costs)
    
    while True:
        us, vs = get_us_and_vs(bfs, balanced_costs)
        ws = get_ws(bfs, balanced_costs, us, vs)
        if not can_be_improved(ws):
            break
        ev_position = get_entering_variable_position(ws)
        loop = get_loop([p for p, v in bfs], ev_position)
        bfs = loop_pivoting(bfs, loop)

    # Create the optimal solution matrix with the correct dimensions
    ans = np.zeros((len(balanced_costs), len(balanced_costs[0])))
    for (i, j), v in bfs:
        ans[i][j] = int(v)
    
    print("\nOptimal solution using MODI's method:")
    headers = [f'Demand {i+1}' for i in range(len(balanced_demand))]
    num_cols = len(ans[0])
    print(tabulate(ans, headers, tablefmt="grid", colalign=("center",) * num_cols))
    return ans

def get_balanced(supply, demand, costs):
    total_supply = sum(supply)
    total_demand = sum(demand)

    if total_supply < total_demand:
        # Add a dummy row with zero costs to balance the problem
        new_supply = supply + [total_demand - total_supply]
        new_costs = costs + [[0] * len(demand)]
        return new_supply, demand, new_costs
    elif total_supply > total_demand:
        # Add a dummy column with zero costs to balance the problem
        new_demand = demand + [total_supply - total_demand]
        new_costs = costs + [[0] * (len(demand) + 1) for _ in range(len(supply))]
        return supply, new_demand, new_costs
    else:
        return supply, demand, costs

def get_total_cost(costs, ans):
    total_cost = 0
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            total_cost += cost * ans[i][j]
    return total_cost
 
def get_us_and_vs(bfs, costs): 
    us = [None] * len(costs) 
    vs = [None] * len(costs[0]) 
    us[0] = 0 
    bfs_copy = bfs.copy() 
 
    while len(bfs_copy) > 0: 
        for index, bv in enumerate(bfs_copy): 
            i, j = bv[0] 
            if us[i] is None and vs[j] is None: 
                continue 
            cost = costs[i][j] 
            if us[i] is None: 
                us[i] = cost - vs[j] 
            else: 
                vs[j] = cost - us[i] 
            bfs_copy.pop(index) 
            break 
    return us, vs 
 
def get_ws(bfs, costs, us, vs): 
    ws = [] 
    for i, row in enumerate(costs): 
        for j, cost in enumerate(row): 
            non_basic = all([p[0] != i or p[1] != j for p, v in bfs]) 
            if non_basic: 
                ws.append(((i, j), us[i] + vs[j] - cost)) 
    return ws 
 
def can_be_improved(ws): 
    return any(v > 0 for p, v in ws) 
 
def get_entering_variable_position(ws): 
    return max(ws, key=lambda w: w[1])[0] 
 
def get_possible_next_nodes(loop, not_visited): 
    last_node = loop[-1] 
    nodes_in_row = [n for n in not_visited if n[0] == last_node[0]] 
    nodes_in_column = [n for n in not_visited if n[1] == last_node[1]] 
    if len(loop) < 2: 
        return nodes_in_row + nodes_in_column 
    else: 
        prev_node = loop[-2] 
        row_move = prev_node[0] == last_node[0] 
        if row_move: 
            return nodes_in_column 
        return nodes_in_row 
 
def get_loop(bv_positions, ev_position): 
    def inner(loop): 
        if len(loop) > 3: 
            can_be_closed = len(get_possible_next_nodes(loop, [ev_position])) == 1 
            if can_be_closed: 
                return loop 
        not_visited = list(set(bv_positions) - set(loop)) 
        possible_next_nodes = get_possible_next_nodes(loop, not_visited) 
        for next_node in possible_next_nodes: 
            new_loop = inner(loop + [next_node]) 
            if new_loop: 
                return new_loop 
    return inner([ev_position]) 
 
def loop_pivoting(bfs, loop): 
    even_cells = loop[0::2] 
    odd_cells = loop[1::2] 
    get_bv = lambda pos: next(v for p, v in bfs if p == pos) 
    leaving_position = sorted(odd_cells, key=get_bv)[0] 
    leaving_value = get_bv(leaving_position) 
    new_bfs = [] 
    for p, v in [bv for bv in bfs if bv[0] != leaving_position] + [(loop[0], 0)]: 
        if p in even_cells: 
            v += leaving_value 
        elif p in odd_cells: 
            v -= leaving_value 
        new_bfs.append((p, v)) 
    return new_bfs 

if _name_ == "_main_":
    rows = int(input("Enter the number of rows (supplies): "))
    cols = int(input("Enter the number of columns (demands): "))
    print("Enter the cost matrix row by row (separated by space):")
    cost = []
    for i in range(rows):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        cost.append(row)
    print("Enter the supply values (separated by space):")
    supply = list(map(int, input().split()))
    print("Enter the demand values (separated by space):")
    demand = list(map(int, input().split()))
    
    if sum(supply) != sum(demand):
        print("\nNot Balanced")
    else:
        print("\nBalanced")
        
        # Directly call MODI's method which internally calls NWCR
    print("\n--- Applying NWCR and MODI's Method to find the Optimal Solution ---")
    ans = modi_method(cost, supply, demand)
    optimal_cost = get_total_cost(cost, ans)
    print(f"\nTotal optimal cost: {optimal_cost}")