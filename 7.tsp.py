labels = []

def calculatePathWeight(path, graph):
    total_weight = 0
    for i in range(len(path) - 1):
        total_weight += graph[path[i]][path[i + 1]]
    total_weight += graph[path[-1]][path[0]]
    return total_weight

def index_to_label(index):
    return labels[index]

def convert_indices_to_labels(indices):
    return [index_to_label(index) for index in indices]

def print_matrix_with_labels(graph):
    print("\nDistance Matrix:")
    print("      ", end="")
    for label in labels:
        print(f"{label:4}", end="")
    print()
    
    print("   ", end="")
    print("-" * (4 * len(labels)))
    
    for i, row in enumerate(graph):
        print(f"{labels[i]} |", end="")
        for value in row:
            print(f"{value:4}", end="")
        print()
    print()

def travellingSalesmanProblem(graph):
    V = len(graph)
    vertices = list(range(V))
    min_path_weight = float('inf')
    min_path = []
    
    def generate_permutations(arr, i):
        if i == len(arr):
            nonlocal min_path_weight, min_path
            path_weight = calculatePathWeight(arr, graph)
            if path_weight < min_path_weight:
                min_path_weight = path_weight
                min_path = arr[:]
        else:
            for j in range(i, len(arr)):
                arr[i], arr[j] = arr[j], arr[i]
                generate_permutations(arr, i + 1)
                arr[i], arr[j] = arr[j], arr[i]
    
    generate_permutations(vertices, 0)
    return min_path, min_path_weight

def main():
    V = int(input("Enter the number of cities: "))
    
    for i in range(V):
        labels.append(chr(ord('A') + i))
    
    graph = []
    print("\nEnter the distance between cities (space-separated values):")
    print("Enter 0 for same city and -1 if no direct path exists")
    for i in range(V):
        print(f"Enter distances from city {labels[i]}: ", end="")
        row = list(map(int, input().split()))
        graph.append(row)
    
    print_matrix_with_labels(graph)
    
    min_path, min_path_weight = travellingSalesmanProblem(graph)
    
    min_path = convert_indices_to_labels(min_path)
    
    print("Minimum Travelling cost:", min_path_weight)
    print("Optimal Travelling plan:")
    for i in range(len(min_path) - 1):
        print(min_path[i], "->", min_path[i + 1])
    print(min_path[-1], "->", min_path[0])

if __name__ == "__main__":
    main()

'''
Enter the number of cities:  4

Enter the distance between cities (space-separated values):
Enter 0 for same city and -1 if no direct path exists
Enter distances from city A:  0 4 9 5
Enter distances from city B:  6 0 4 8
Enter distances from city C:  9 4 0 9
Enter distances from city D:  5 8 9 0

Distance Matrix:
      A   B   C   D   
   ----------------
A |   0   4   9   5
B |   6   0   4   8
C |   9   4   0   9
D |   5   8   9   0

Minimum Travelling cost: 22
Optimal Travelling plan:
A -> B
B -> C
C -> D
D -> A

'''