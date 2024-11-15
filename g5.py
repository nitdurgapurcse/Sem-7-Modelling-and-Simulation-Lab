'''
max z = 40x+80y
subject to,
2x+3y<=48
x<=15
y<=10
'''

import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from math import ceil

# drawing the grid and fixing size
d = np.linspace(0, 150, 1000)
x, y = np.meshgrid(d, d)

# Define the inequalities
inequality1 = (y <= (48 - 2*x)/3)    # 2x+3y<=48
inequality2 = (y <= 10)              # y<=10
inequality3 = (x <= 15)              # x<=15

# fixing figure size
plt.figure(figsize=(10, 8))

# Line 1: 2x+3y<=48
x1 = [0, 24]
y1 = [16, 0]
plt.plot(x1, y1, label="$2x+3y<=48$")

# Line 2: x = 15 (vertical line)
plt.axvline(x=15, color='b', label="$x<=15$")

# Line 3: y = 10 (horizontal line)
plt.axhline(y=10, color='g', label="$y<=10$")

# Plot the feasible region
plt.imshow((inequality1 & inequality2 & inequality3 ).astype(int),
           extent=(d.min(), d.max(),d.min(), d.max()),
           origin="lower", cmap="Greys", alpha=0.3)

# Find intersection points
line1 = LineString([(0, 24), (16, 0)])      # 2x+3y<=48
line2 = LineString([(15, 0), (15, 200)])    # x = 15
line3 = LineString([(0, 10), (200, 10)])    # y = 10

# Get all intersection points
intersections = []

# Intersection of 2x+3y<=48 and x = 15
int1 = line1.intersection(line2)
if not int1.is_empty:
    intersections.append((15, 6))

# Intersection of 2x+3y<=48 and y = 10
int2 = line1.intersection(line3)
if not int2.is_empty:
    intersections.append((9, 10))

intersections.append((0,0))
intersections.append((15,0))
intersections.append((0,10))

# Plot intersection points
for point in intersections:
    plt.plot(point[0], point[1], 'ro')

plt.xlim(0, 30)
plt.ylim(0, 30)
plt.xlabel(r'$x - axis$')
plt.ylabel(r'$y - axis$')
plt.title('Linear Programming Problem Visualization')
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout()
plt.show()

# Calculate Z value at each corner point
z_values = []
p,q=int1.xy
points=[(int(p[0]),int(q[0]))]
for point in intersections:
    z = 40*point[0] + 80*point[1]
    z_values.append((z, point))
    print(f"At point {point}: Z = {z}")

# Find the maximum Z value and its corresponding point
max_z, max_point = max(z_values, key=lambda item: item[0])

print('\nResults:')
print(f'Maximum value of Z is {max_z}')
print(f'Optimal solution occurs at point {max_point}')