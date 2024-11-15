import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from math import ceil

# Define the meshgrid
d = np.linspace(0, 250, 3000)
x, y = np.meshgrid(d, d)

# Define the inequalities
inequality1 = (y <= (200 - x)/3)     # x + 3y <= 200
inequality2 = (y <= 100 - x)         # x + y <= 100
inequality3 = (x >= 20)              # x >= 20
inequality4 = (y >= 10)              # y >= 10

# Plot lines
plt.figure(figsize=(10, 8))

# Line 1: x + 3y = 200
x1 = [0, 200]
y1 = [200/3, 0]
plt.plot(x1, y1, label="$x+3y=200$")

# Line 2: x + y = 100
x2 = [0, 100]
y2 = [100, 0]
plt.plot(x2, y2, label="$x+y=100$")

# Line 3: x = 20 (vertical line)
plt.axvline(x=20, color='b', label="$x=20$")

# Line 4: y = 10 (horizontal line)
plt.axhline(y=10, color='g', label="$y=10$")

# Plot the feasible region
plt.imshow((inequality1 & inequality2 & inequality3 & inequality4).astype(int),
           extent=(d.min(), d.max(), d.min(), d.max()),
           origin="lower", cmap="Greys", alpha=0.3)

# Find intersection points
line1 = LineString([(0, 200/3), (200, 0)])  # x + 3y = 200
line2 = LineString([(0, 100), (100, 0)])    # x + y = 100
line3 = LineString([(20, 0), (20, 200)])    # x = 20
line4 = LineString([(0, 10), (200, 10)])    # y = 10

# Get all intersection points
intersections = []

# Intersection of x + 3y = 200 and x = 20
int1 = line1.intersection(line2)
if not int1.is_empty:
    intersections.append((20, (200-20)/3))

# Intersection of x + 3y = 200 and y = 10
int2 = line1.intersection(line4)
if not int2.is_empty:
    intersections.append((200-30, 10))

# Intersection of x + y = 100 and x = 20
int3 = line2.intersection(line3)
if not int3.is_empty:
    intersections.append((20, 80))

# Intersection of x + y = 100 and y = 10
int4 = line2.intersection(line4)
if not int4.is_empty:
    intersections.append((90, 10))

# Plot intersection points
for point in intersections:
    plt.plot(point[0], point[1], 'ro')

plt.xlim(0, 250)
plt.ylim(0, 100)
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
points=[(ceil(p[0]),int(q[0]))]
for point in points:

    
    z = 30*point[0] + 50*point[1]
    z_values.append((z, point))
    print(f"At point {point}: Z = {z}")

# Find the maximum Z value and its corresponding point
max_z, max_point = max(z_values, key=lambda item: item[0])

print('\nResults:')
print(f'Maximum value of Z is {max_z}')
print(f'Optimal solution occurs at point {max_point}')