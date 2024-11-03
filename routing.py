import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
from matplotlib.animation import FuncAnimation

# Set random seed and initialize variables
np.random.seed(0)
n = 7  # Number of clients
Q = 15  # Vehicle capacity (adjusted to demonstrate capacity constraint)
N = [chr(ord('b') + i) for i in range(n)]  # Client nodes [b,c,d]
V = ['a'] + N  # All nodes including depot [0,1,2,3,4,5]

# Generate random demands and locations
q = {i: np.random.randint(1, 10) for i in N}  # Random demands between 1 and 10
loc_x = np.random.randint(0, 101, size=n + 1).tolist()  # Random x coordinate
loc_y = np.random.randint(0, 101, size=n + 1).tolist()  # Random y coordinate


# Set up plot
plt.figure(figsize=(4, 4))
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.gca().set_aspect('equal', adjustable='box')

# Set gridlines every 10 units
plt.grid(visible=True, which='major', color='gray', linestyle='-', linewidth=0.5)
plt.xticks(range(0, 101, 10))  # Set grid interval for x-axis
plt.yticks(range(0, 101, 10))  # Set grid interval for y-axis

# Remove tick labels
plt.gca().set_xticklabels([])  # Remove x-axis labels
plt.gca().set_yticklabels([])  # Remove y-axis labels


# Generate points based on loc_x and loc_y, adjusting based on n
points = {'a': (loc_x[0], loc_y[0])}  # Initialize with depot

# Loop through clients to add them to the points dictionary
for i in range(1, n + 1):
    points[chr(ord('b') + (i - 1))] = (loc_x[i], loc_y[i])  # Generate keys 'b', 'c', etc.

points_string = ''

for letters in points:
    points_string += letters

new_points_string = points_string[1:]

# Initialize lists and variables for route storage
perm_result = []
modified_permutations = []
path_distances = {}
valid_paths = []
shortest_path = []
shortest_path_dist = float('inf')

def get_permutations(s, num_a):
    # Generate all permutations of the input string
    global perm_result
    perm = permutations(s + 'a'* num_a)
    
    # Convert permutations from tuples to strings and remove duplicates
    perm_strings = {''.join(p) for p in perm}

    step2_perm_strings = perm_strings.copy()

    #get rid of strings that start or end with a
    for string in perm_strings:
        if string[0]== 'a' or string[-1] == 'a':
            step2_perm_strings.remove(string)  
    
    #get rid of strings that have consecutive a's
    step3_perm_strings = step2_perm_strings.copy()
    set_char = 'b' 

    for string in step2_perm_strings:
        for char_ind in range(len(string)-1):
            if string[char_ind] == 'a' and set_char == 'a':
                step3_perm_strings.remove(string)
                break
            set_char = string[char_ind]

    #(len(list(step3_perm_strings)))
    perm_result.extend(step3_perm_strings)
    return list(step3_perm_strings)  # Return as a list

for i in range(1,n):
    get_permutations(new_points_string, i)

modified_permutations = ['a' + perm + 'a' for perm in perm_result]

print(len(modified_permutations))


# Function to calculate Euclidean distance
def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to calculate the total distance of a given path
def calculate_path_distance(path, coords):
    total_distance = 0.0
    for i in range(len(path) - 1):
        point1 = coords[path[i]]
        point2 = coords[path[i + 1]]
        total_distance += euclidean_distance(point1, point2)
    return total_distance

path_distances = {}

# Calculate distance for each path and store in the dictionary
for path in modified_permutations:
    distance = calculate_path_distance(path, points)
    path_distances[path] = distance

# Print the dictionary with path distances
#print(path_distances)

veh_hold = 0 

valid_paths = []

def cap_verify(path_list):
    for i in path_list:
        veh_hold = 0
        for ii in range(len(i)-1):
            if i[ii] == 'a':
                veh_hold = 0
            else:
                veh_hold += q[i[ii]]
                if veh_hold > Q:
                    break 
        else:  # This runs only if the inner loop didn’t hit a break
            valid_paths.append(i)
    #print(valid_paths)

shortest_path = []
shortest_path_dist = 10000000

def find_shortest(path_list):
    global shortest_path_dist
    for i in path_list:
        if path_distances[i] < shortest_path_dist:
            shortest_path_dist = path_distances[i]
            shortest_path.append(i)
    print(shortest_path[-1])
    print(shortest_path_dist)

cap_verify(modified_permutations)
find_shortest(valid_paths)

final_shortest_path = shortest_path[-1]

numeric_representation = ''.join(str(ord(char) - ord('a')) for char in final_shortest_path)
number_list = [int(digit) for digit in numeric_representation]

for i in range(len(number_list) - 1):
    start_index = number_list[i]
    end_index = number_list[i + 1]
    #plt.plot([loc_x[start_index], loc_x[end_index]], [loc_y[start_index], loc_y[end_index]], color='blue', linestyle='dashed')
    
    plt.annotate('', 
                 xy=(loc_x[end_index], loc_y[end_index]), 
                 xytext=(loc_x[start_index], loc_y[start_index]),
                 arrowprops=dict(arrowstyle='-', color='blue'))

plt.scatter(loc_x[1:], loc_y[1:], c='black')
plt.plot(loc_x[0], loc_y[0], c='r', marker='s')  # Plot the depot location

alph_list = ['a','b','c','d','e','f','g']

#for i in N:
#    idx = V.index(i)  # Get the index of the letter in V
#    plt.annotate(f'${alph_list[idx-1]}={q[i]}$', (loc_x[idx] + 2, loc_y[idx]))  # Add demand labels

letters = ['a','b','c','d','e','f','g']
plt.annotate(f'${letters[0]}={q["b"]}$', (loc_x[1] + 3, loc_y[1]))
plt.annotate(f'${letters[1]}={q["c"]}$', (loc_x[2] + 2, loc_y[2]))
plt.annotate(f'${letters[2]}={q["d"]}$', (loc_x[3]-2, loc_y[3]+3))
plt.annotate(f'${letters[3]}={q["e"]}$', (loc_x[4] + 2, loc_y[4]))
plt.annotate(f'${letters[4]}={q["f"]}$', (loc_x[5] + 1, loc_y[5]+2))
plt.annotate(f'${letters[5]}={q["g"]}$', (loc_x[6] + 2, loc_y[6]))
plt.annotate(f'${letters[6]}={q["h"]}$', (loc_x[7] + 2, loc_y[7]))


keys_with_target_value = [key for key, value in path_distances.items() if value == shortest_path_dist]
print(keys_with_target_value)

plt.annotate(f'$Depot$', (loc_x[0] + 3, loc_y[0]))

plt.show()








