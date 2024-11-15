def VAM():
  # Input for supply and demand cities
  n = int(input("Enter number of supply cities: "))
  m = int(input("Enter number of demand cities: "))
  supply_cities = []
  for i in range(n):
    city = input(f"Enter name of supply city {i+1}: ")
    supply = int(input(f"Enter max supply for {city}: "))
    supply_cities.append((city, supply))

  demand_cities = []
  for i in range(m):
    city = input(f"Enter name of demand city {i+1}: ")
    demand = int(input(f"Enter max demand for {city}: "))
    demand_cities.append((city, demand))

  # Input for transportation costs
  costs = []
  for s_city, _ in supply_cities:
    row = []
    for d_city, _ in demand_cities:
      cost = int(input(f"Enter cost from {s_city} to {d_city}: "))
      row.append(cost)
    costs.append(row)

  # Initialize allocation matrix
  allocations = [[0 for _ in range(m)] for _ in range(n)]

  # Initialize supply and demand lists (extracting values from tuples)
  supply = [s[1] for s in supply_cities]
  demand = [d[1] for d in demand_cities]

  INF = 10**3
  n = len(costs)
  m = len(costs[0])
  ans = 0

  def findDiff(grid):
    rowDiff = []
    colDiff = []
    for i in range(len(grid)):
      arr = grid[i][:]
      arr.sort()
      rowDiff.append(arr[1] - arr[0] if len(arr) > 1 else 0)  # Handle single-element rows
    col = 0
    while col < len(grid[0]):
      arr = []
      for i in range(len(grid)):
        arr.append(grid[i][col])
      arr.sort()
      col += 1
      colDiff.append(arr[1] - arr[0] if len(arr) > 1 else 0)  # Handle single-element columns
    return rowDiff, colDiff

  while max(supply) != 0 or max(demand) != 0:
    row, col = findDiff(costs)
    maxi1 = max(row)
    maxi2 = max(col)

    if maxi1 >= maxi2:
      for ind, val in enumerate(row):
        if val == maxi1:
          mini1 = min(costs[ind])
          for ind2, val2 in enumerate(costs[ind]):
            if val2 == mini1:
              mini2 = min(supply[ind], demand[ind2])
              allocations[ind][ind2] = mini2  # Update allocation matrix
              ans += mini2 * mini1
              supply[ind] -= mini2
              demand[ind2] -= mini2
              if demand[ind2] == 0:
                for r in range(n):
                  costs[r][ind2] = INF
              else:
                costs[ind] = [INF for i in range(m)]
              break
          break
    else:
      for ind, val in enumerate(col):
        if val == maxi2:
          mini1 = INF
          for j in range(n):
            mini1 = min(mini1, costs[j][ind])

          for ind2 in range(n):
            val2 = costs[ind2][ind]
            if val2 == mini1:
              mini2 = min(supply[ind2], demand[ind])
              allocations[ind2][ind] = mini2  # Update allocation matrix
              ans += mini2 * mini1
              supply[ind2] -= mini2
              demand[ind] -= mini2
              if demand[ind] == 0:
                for r in range(n):
                  costs[r][ind] = INF
              else:
                costs[ind2] = [INF for i in range(m)]
              break
          break

  print("The basic feasible solution is ", ans)
  print("\nAllocation Matrix:")
  for row in allocations:
    print(row)

VAM()

'''
Enter number of supply cities: 3
Enter number of demand cities: 4
Enter name of supply city 1: a
Enter max supply for a: 100
Enter name of supply city 2: b
Enter max supply for b: 150
Enter name of supply city 3: c
Enter max supply for c: 200
Enter name of demand city 1: x
Enter max demand for x: 80
Enter name of demand city 2: y
Enter max demand for y: 120
Enter name of demand city 3: z
Enter max demand for z: 100
Enter name of demand city 4: w
Enter max demand for w: 150
Enter cost from a to x: 5
Enter cost from a to y: 8
Enter cost from a to z: 6
Enter cost from a to w: 9
Enter cost from b to x: 7
Enter cost from b to y: 4
Enter cost from b to z: 3
Enter cost from b to w: 8
Enter cost from c to x: 6
Enter cost from c to y: 7
Enter cost from c to z: 4
Enter cost from c to w: 5
The basic feasible solution is  2040

Allocation Matrix:
[80, 0, 20, 0]
[0, 120, 30, 0]
[0, 0, 50, 150]
'''