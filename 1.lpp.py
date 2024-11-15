import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Define the coefficients of the objective function
c = [2, 3]

# Define the inequality constraints matrix
A = [[-10, -5],
     [-5, -10]]

# Define the inequality constraints vector
b = [-50, -40]

# Define the bounds for x and y
x_bounds = (0, None)
y_bounds = (0, None)

# Solve the linear programming problem
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

# Extract the optimal solution
optimal_x = res.x[0]
optimal_y = res.x[1]
minimum_cost = res.fun

# Print the results
print('Optimal number of servings for Food A:', optimal_x)
print('Optimal number of servings for Food B:', optimal_y)
print('Minimum cost:', minimum_cost)

# Plotting the feasible region and constraints
x = np.linspace(0, 10, 400)
y1 = (50 - 10*x) / 5
y2 = (40 - 5*x) / 10

plt.plot(x, y1, label=r'$10x + 5y \geq 50$')
plt.plot(x, y2, label=r'$5x + 10y \geq 40$')

plt.xlim((0, 10))
plt.ylim((0, 10))
plt.xlabel('Servings of Food A (x)')
plt.ylabel('Servings of Food B (y)')

# Fill the feasible region
plt.fill_between(x, y1, 10, where=(y1 <= 10), color='white', alpha=0.3)
plt.fill_between(x, y2, 10, where=(y2 <= 10), color='white', alpha=0.3)

# Mark the feasible region explicitly
plt.fill_between(x, np.maximum(y1, y2), 10, color='green', alpha=0.5)

# Plotting the optimal solution
plt.scatter(optimal_x, optimal_y, color='red', marker='o', label=f'Optimal solution ({optimal_x:.2f}, {optimal_y:.2f})')
plt.legend()

# Display the graph
plt.show()

'''
Optimal number of servings for Food A: 4.0
Optimal number of servings for Food B: 2.0
Minimum cost: 14.0
'''