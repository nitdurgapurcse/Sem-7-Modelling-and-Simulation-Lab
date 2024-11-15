import sys

# VAM
def isDegenerate(m, n, l):
  if m+n-1 == l:
    # Not degenrate
    return False
  else:
    # Degenerate
    return True

class transportationProblem:

	def __init__(self, supply, demand, cost_matrix):

		self.supply = supply
		self.demand = demand
		self.cost_matrix = cost_matrix
		self.ans = []
		self.total_cost = 0

	def getLowest(self, arr):

		temp_min = 0
		for i in range(len(arr)):
			if arr[i] < arr[temp_min]:
				temp_min = i

		return arr[temp_min]

	def getSecondLowest(self, arr, l):

		min_ele = arr.index(l)

		temp_min = 0
		if min_ele == 0:
			temp_min = 1

		for i in range(len(arr)):
			if arr[i] < arr[temp_min] and i!=min_ele:
				temp_min = i

		return arr[temp_min]

	def transpose(self, arr):

		temp = [[arr[i][j] for i in range(len(arr))] for j in range(len(arr[0]))]
		return temp

	def isBalanced(self): # To check if the transportation problem is balanced

		self.balanced = False
		if sum(self.demand) == sum(self.supply):
			self.balanced = True

	def vam(self): # To find intial feasible solution using VAM (Vogel's Approximation Method)

		cost_matrix = [[self.cost_matrix[i][j] for j in range(len(self.cost_matrix[0]))] for i in range(len(self.cost_matrix))]

		supply = [i for i in self.supply]
		demand = [i for i in self.demand]

		sd_left = len(supply) + len(demand)

		while sd_left>1:

			row_diff = []
			col_diff = []

			for j in cost_matrix:

				min_ele = self.getLowest(j)
				sec_min_ele = self.getSecondLowest(j, min_ele)

				row_diff.append( sec_min_ele - min_ele )

			t_cost_matrix = self.transpose(cost_matrix)

			for j in t_cost_matrix:

				min_ele = self.getLowest(j)
				sec_min_ele = self.getSecondLowest(j, min_ele)

				col_diff.append( sec_min_ele - min_ele )

			max_row_diff = max(row_diff)
			max_col_diff = max(col_diff)

			# ic(row_diff, col_diff)

			if max_row_diff > max_col_diff:

				# ic("Case 1")

				row_index = row_diff.index(max_row_diff)
				# ic(row_index)
				row = cost_matrix[row_index]
				# ic(row)
				row_min = min(row)
				row_min_index = row.index(row_min)
				# ic(row_min, row_min_index)

				if supply[row_index] > demand[row_min_index]:
					# ic()
					self.ans.append([ demand[row_min_index] , row_min , (row_index, row_min_index)])

					supply[row_index] -= demand[row_min_index]
					demand[row_min_index] = 0

					for i in cost_matrix:
						i[row_min_index] = sys.maxsize

					sd_left -= 1

				elif supply[row_index] < demand[row_min_index]:
					# ic()
					self.ans.append([ supply[row_index] , row_min , (row_index, row_min_index)])

					demand[row_min_index] -= supply[row_index]
					supply[row_index] = 0

					cost_matrix[row_index] = [sys.maxsize for i in range(len(cost_matrix[0]))]
					sd_left -= 1

				else:
					# ic()
					self.ans.append([ supply[row_index] , row_min , (row_index, row_min_index)])

					demand[row_min_index] = 0
					supply[row_index] = 0

					for i in cost_matrix:
						i[row_min_index] = sys.maxsize

					cost_matrix[row_index] = [sys.maxsize for i in range(len(cost_matrix[0]))]
					sd_left -= 2

				# ic(cost_matrix)

			else:

				col_index = col_diff.index(max_col_diff)
				col = t_cost_matrix[col_index]
				col_min = min(col)
				col_min_index = col.index(col_min)

				if supply[col_min_index] > demand[col_index]:

					self.ans.append([ demand[col_index] , col_min , (col_min_index, col_index)])

					supply[col_min_index] -= demand[col_index]
					demand[col_index] = 0

					for i in cost_matrix:
						i[col_index] = sys.maxsize

					sd_left -= 1

				elif supply[col_min_index] < demand[col_index]:

					self.ans.append([ supply[col_min_index] , col_min , (col_min_index, col_index)])

					demand[col_index] -= supply[col_min_index]
					supply[col_min_index] = 0

					cost_matrix[col_min_index] = [sys.maxsize for i in range(len(cost_matrix[0]))]
					sd_left -= 1

				else:

					self.ans.append([ supply[col_min_index] , col_min , (col_min_index, col_index)])

					demand[col_index] = 0
					supply[col_min_index] = 0

					for i in cost_matrix:
						i[col_index] = sys.maxsize

					cost_matrix[col_min_index] = [sys.maxsize for i in range(len(cost_matrix[0]))]
					sd_left -= 1

			# ic(self.ans)
		return self.ans

	def getTotalCost(self):

		for i in self.ans:
			self.total_cost += i[0] * i[1]

		return self.total_cost


def get_uv(bfs, cost_matrix, default):
  u = [None] * len(cost_matrix)
  v = [None] * len(cost_matrix[0])

  u[default] = 0
  bfs_copy = bfs.copy()

  while len(bfs_copy)>0:
    for index, bv in enumerate(bfs_copy):
      i, j = bv[2]

      if u[i] is None and v[j] is None:
        continue

      c_ij = cost_matrix[i][j]
      if u[i] is None:
        u[i] = c_ij - v[j]
      if v[j] is None:
        v[j] = c_ij - u[i]

      bfs_copy.pop(index)
      break

  return u, v

def get_d(bfs, cost_matrix, u, v):
  d = []
  allocated_cells = [bfs[i][2] for i in range(len(bfs))]

  for i in range(len(cost_matrix)):
    for j in range(len(cost_matrix[0])):
      if (i,j) not in allocated_cells:
        c_ij = cost_matrix[i][j]
        d_ij = c_ij - u[i] - v[j]
        d.append([d_ij,(i,j)])

  return d

def get_min_index(d):
  min_index = 0
  min_val = d[0][0]
  for i in range(len(d)):
    if d[i][0] < min_val:
      min_val = d[i][0]
      min_index = i
  return min_index

def get_loop(bfs, p_row, p_col):

  loop_indices = [(p_row, p_col)]
  assigned = [i[2] for i in bfs]
  # ic(assigned)

  same_row_assignments = []
  same_col_assignments = []

  for assignment in assigned:
    if assignment[0] == p_row:
      same_row_assignments.append(assignment)
    if assignment[1] == p_col:
      same_col_assignments.append(assignment)

  # ic(same_row_assignments)
  # ic(same_col_assignments)

  for i in same_row_assignments:
    fl = 0
    for j in same_col_assignments:
      if (j[0],i[1]) in assigned:
        # ic(j[0],i[1])
        loop_indices.append(i)
        loop_indices.append(j)
        loop_indices.append((j[0],i[1]))
        fl = 1
        break
    if fl==1:
      return loop_indices

  return None

bfs = [[80, 5, (2, 4)], [40, 4, (4, 1)], [50, 5, (0, 3)], [50, 4, (0, 0)], [10, 5, (4, 2)], [60, 8, (3, 2)], [10, 9, (1, 0)], [20, 11, (1, 4)], [30, 19, (1, 2)]]
p_row, p_col = 2, 1
get_loop(bfs, p_row, p_col)

def improve(cost_matrix, bfs, d):
  min_index = get_min_index(d)
  # ic(min_index)

  p_row,p_col = d[min_index][1]

  loop_indices = get_loop(bfs, p_row, p_col)
  if loop_indices == None:
    return None

  # ic(loop_indices)

  bfs_dict = {}
  for i in bfs:
    bfs_dict[i[2]] = [i[0], i[1]]
  # ic(bfs_dict)

  # min_alloc = float("Inf")
  min_alloc = min(bfs_dict[loop_indices[1]][0],
                  bfs_dict[loop_indices[2]][0])

  # ic(min_alloc)

  bfs_dict[loop_indices[0]] = [min_alloc, cost_matrix[loop_indices[0][0]][loop_indices[0][1]]]
  bfs_dict[loop_indices[1]][0] -= min_alloc
  bfs_dict[loop_indices[2]][0] -= min_alloc
  bfs_dict[loop_indices[3]][0] += min_alloc

  # ic(bfs_dict)

  new_bfs = []
  for key, val in bfs_dict.items():
    if val[0] != 0:
      new_bfs.append([val[0], val[1], key])

  # ic(new_bfs)
  return new_bfs

def MODI(supply, demand, cost_matrix, bfs):

  default = 0
  # for i in range(2):
  while True:
    u,v = get_uv(bfs, cost_matrix, default)
    # ic(u)
    # ic(v)
    d = get_d(bfs, cost_matrix, u, v)
    # ic(d)
    if not any(i[0]<0 for i in d):
      # ic("OPT", bfs)
      return bfs

    temp_bfs = improve(cost_matrix, bfs, d)
    if temp_bfs == None:
      default = default + 1
      if default == len(u):
        # print("*Complex closed path")
        return None
    else:
      bfs = temp_bfs

# supply = [100,60,80,60,50]
# demand = [60,40,100,50,100]
# cost_matrix = [[4,9,10,5,13],[9,17,19,9,11],[12,3,9,7,5],[6,17,8,14,10],[7,4,5,15,12]]
# bfs = [[80, 5, (2, 4)], [40, 4, (4, 1)], [50, 5, (0, 3)], [50, 4, (0, 0)], [10, 5, (4, 2)], [60, 8, (3, 2)], [10, 9, (1, 0)], [20, 11, (1, 4)], [30, 19, (1, 2)]]
# MODI(supply, demand, cost_matrix, bfs)

# Main

def calculate_cost(fs):
  cost = 0
  for i in fs:
    cost += i[0]*i[1]
  return cost

# from tp import transportationProblem

def tc(n):

	if n==1: # Answer = 779
		supply = list(map(int, input("Enter supply").split()))
		demand = list(map(int, input("Enter demand").split()))
		cost_matrix = []
		n = int(input("Enter number of rows: "))
		for i in range(n):
			cost_matrix.append(list(map(int, input("Enter row: ").split())))
	return [supply, demand, cost_matrix]


supply, demand, cost_matrix = tc(1)
TP = transportationProblem(supply, demand, cost_matrix)
bfs = TP.vam()
print("\nBasic feasible solution:")
print("Cost: ", TP.getTotalCost())
print("Assignment:\n", bfs)
if isDegenerate(len(supply), len(demand), len(bfs)):
	print("\n*Basic feasible solution is degenerate*")
else:
	ops = MODI(supply, demand, cost_matrix, bfs)
	print("\nOptimal solution:")
	if ops == None:
		print("*Complex closed path")
	else:
		print("Cost: ", calculate_cost(ops))
		print("Assignment:\n", ops)
print("")
print("")

'''
Enter supply7 9 18
Enter demand5 8 7 14
Enter number of rows: 3
Enter row: 19 30 50 10
Enter row: 70 30 40 60
Enter row: 40 8 70 20

Basic feasible solution:
Cost:  779
Assignment:
 [[8, 8, (2, 1)], [5, 19, (0, 0)], [10, 20, (2, 3)], [2, 10, (0, 3)], [7, 40, (1, 2)], [2, 60, (1, 3)]]

Optimal solution:
Cost:  743
Assignment:
 [[6, 8, (2, 1)], [5, 19, (0, 0)], [12, 20, (2, 3)], [2, 10, (0, 3)], [7, 40, (1, 2)], [2, 30, (1, 1)]]


'''