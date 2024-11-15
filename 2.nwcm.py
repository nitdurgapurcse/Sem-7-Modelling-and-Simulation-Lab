def north_west_corner_method():
 """
This function implements the North-West Corner Method (NWCM) for solving
transportation problems. It takes input as matrices for supply, demand,
and transportation costs. The function then calculates the optimal
allocation of goods to minimize the total transportation cost.

 """

 # Input for supply and demand cities
 print("Enter the number of supply cities and demand cities (separated by space):")
 num_supply_cities, num_demand_cities = map(int, input().split())

 # Input for supply city names and supplies
 print("Enter the names and supplies of the supply cities (e.g., 'City1 10 City2 20'): ")
 supply_cities = []
 supply_city_names = input().split()
 for i in range(0, len(supply_city_names), 2):
   supply_cities.append((supply_city_names[i], int(supply_city_names[i+1])))

 # Input for demand city names and demands
 print("Enter the names and demands of the demand cities (e.g., 'City1 10 City2 20'): ")
 demand_cities = []
 demand_city_names = input().split()
 for i in range(0, len(demand_city_names), 2):
   demand_cities.append((demand_city_names[i], int(demand_city_names[i+1])))

 # Input for transportation cost matrix
 print("Enter the transportation cost matrix (row-wise, separated by space):")
 transportation_costs = []
 for i in range(num_supply_cities):
   row = list(map(int, input().split()))
   transportation_costs.append(row)

 # Initialize allocation matrix
 allocation_matrix = [[0 for _ in range(num_demand_cities)] for _ in range(num_supply_cities)]

 # Perform North West Corner Method algorithm
 total_cost = 0
 i = 0
 j = 0
 while i < num_supply_cities and j < num_demand_cities:
   supply = supply_cities[i][1]
   demand = demand_cities[j][1]
   allocation = min(supply, demand)
   allocation_matrix[i][j] = allocation
   total_cost += allocation * transportation_costs[i][j]

   if supply < demand:
     demand_cities[j] = (demand_cities[j][0], demand - allocation)
     i += 1
   else:
     supply_cities[i] = (supply_cities[i][0], supply - allocation)
     j += 1

 # Check if solution is non-degenerate (i.e., total number of allocations is equal to row+col-1)
 total_allocations = sum(1 for row in allocation_matrix for allocation in row if allocation > 0)
 if total_allocations == num_supply_cities + num_demand_cities - 1:
   print("The solution is non-degenerate. (Number of allocations = m + n - 1)")

 else:
   print("The solution is degenerate.")

 # Check if solution is balanced (i.e., total supply is equal to total demand)
 total_supply = sum(supply for _, supply in supply_cities)
 total_demand = sum(demand for _, demand in demand_cities)
 if total_supply == total_demand:
   print("The solution is balanced.")
 else:
   print("The solution is not balanced.")

 # Print results
 print("\nAllocation Matrix:")
 for i, row in enumerate(allocation_matrix):
   print(f"Supply City {supply_cities[i][0]}: {row}")
 print("\nTotal Transportation Cost: $", total_cost)

north_west_corner_method()

'''
Enter the number of supply cities and demand cities (separated by space):
3 3
Enter the names and supplies of the supply cities (e.g., 'City1 10 City2 20'): 
w1 20 w2 30 w3 25
Enter the names and demands of the demand cities (e.g., 'City1 10 City2 20'): 
r1 15 r2 25 r3 35
Enter the transportation cost matrix (row-wise, separated by space):
8 6 10
9 12 13
14 9 16
The solution is non-degenerate. (Number of allocations = m + n - 1)
The solution is not balanced.

Allocation Matrix:
Supply City w1: [15, 5, 0]
Supply City w2: [0, 20, 10]
Supply City w3: [0, 0, 25]

Total Transportation Cost: $ 920
'''