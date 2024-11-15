def LCM():
  # input
  n = int(input("Enter number of supply cities: "))
  m = int(input("Enter number of demand cities: "))
  supply_cities = []
  for i in range(n):
    city = input(f"Enter name of supply city {i+1}: ")
    supply = int(input(f"Enter max supply for {city}: "))
    supply_cities.append((city, supply))

  # input for demand cities
  demand_cities = []
  for i in range(m):
    city = input(f"Enter name of demand city {i+1}: ")
    demand = int(input(f"Enter max demand for {city}: "))
    demand_cities.append((city, demand))

  # input for transportation costs
  costs = []
  for s_city, _ in supply_cities:
    row = []
    for d_city, _ in demand_cities:
      cost = int(input(f"Enter cost from {s_city} to {d_city}: "))
      row.append(cost)
    costs.append(row)

  # Initialize allocation matrix
  allocations = [[0 for _ in range(m)] for _ in range(n)]

  # Perform LCM algorithm
  total_cost = 0
  supply_left = sum(s[1] for s in supply_cities)
  demand_left = sum(d[1] for d in demand_cities)

  while supply_left > 0 and demand_left > 0:
    # Find cell with lowest cost
    min_cost = float('inf')
    min_i, min_j = -1, -1
    for i in range(n):
      for j in range(m):
        if costs[i][j] < min_cost and supply_cities[i][1] > 0 and demand_cities[j][1] > 0:
          min_cost = costs[i][j]
          min_i, min_j = i, j

    # Allocate to the cell with lowest cost
    supply = supply_cities[min_i][1]
    demand = demand_cities[min_j][1]
    allocation = min(supply, demand)
    allocations[min_i][min_j] = allocation
    total_cost += allocation * costs[min_i][min_j]

    # Update supply and demand
    supply_cities[min_i] = (supply_cities[min_i][0], supply - allocation)
    demand_cities[min_j] = (demand_cities[min_j][0], demand - allocation)
    supply_left -= allocation
    demand_left -= allocation

  # Print results
  print("\nAllocation Matrix:")
  for row in allocations:
    print(row)

  print("\nTotal Transportation Cost:", total_cost)

LCM()

'''

Enter number of supply cities: 3
Enter number of demand cities: 3
Enter name of supply city 1: s1
Enter max supply for s1: 20
Enter name of supply city 2: s2
Enter max supply for s2: 30
Enter name of supply city 3: s3
Enter max supply for s3: 25
Enter name of demand city 1: r1
Enter max demand for r1: 15
Enter name of demand city 2: r2
Enter max demand for r2: 25
Enter name of demand city 3: r3
Enter max demand for r3: 35
Enter cost from s1 to r1: 8
Enter cost from s1 to r2: 6
Enter cost from s1 to r3: 10
Enter cost from s2 to r1: 9
Enter cost from s2 to r2: 12
Enter cost from s2 to r3: 13
Enter cost from s3 to r1: 14
Enter cost from s3 to r2: 9
Enter cost from s3 to r3: 16

Allocation Matrix:
[0, 20, 0]
[15, 0, 15]
[0, 5, 20]

Total Transportation Cost: 815
'''