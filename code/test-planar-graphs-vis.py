import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from collections import defaultdict

data = []

# Data extraction from stdin
for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue
    tokens = line.split(";")
    
    # Parse the data
    file = tokens[0]
    n = int(tokens[1])
    if tokens[2].startswith("Timeout"):
        bw = -1
    else:
        bw = int(tokens[2])
    bw_bound = int(tokens[3])
    
    # Append to data list
    data.append({"file": file, "n": n, "bw": bw, "bw_bound": bw_bound})

# Extracting values for plotting
n_values = [entry["n"] for entry in data]
bw_values = [entry["bw"] for entry in data]
bw_bound_values = [entry["bw_bound"] for entry in data]

# Count occurrences of (n, bw) pairs
count_dict = defaultdict(int)
for entry in data:
    count_dict[(entry["n"], entry["bw"])] += 1

# Create a list of counts for alpha and size calculation
counts = [count_dict[(n, bw)] for n, bw in zip(n_values, bw_values)]

# Handle empty counts list
if counts:
    max_count = max(counts)
    min_count = min(counts)
    # Normalize counts to range [0, 1]
    normalized_counts = [(count - min_count) / (max_count - min_count) if max_count > min_count else 1 for count in counts]
    # Scale normalized counts to range [0.3, 1.0] for alpha
    alpha_values = [0.3 + 0.7 * alpha for alpha in normalized_counts]
    
    # Scale normalized counts to range [10, 1000] for size
    sizes = [10 + 290 * alpha for alpha in normalized_counts]
else:
    # Default alpha values and sizes if counts list is empty
    alpha_values = [0.3] * len(n_values)
    sizes = [50] * len(n_values)

# Separate values for coloring
n_values_beyond_bound = [n for n, bw in zip(n_values, bw_values) if bw == -1]
bw_values_beyond_bound = [bw for bw in bw_values if bw == -1]
alpha_beyond_bound = [alpha_values[i] for i, bw in enumerate(bw_values) if bw == -1]
sizes_beyond_bound = [sizes[i] for i, bw in enumerate(bw_values) if bw == -1]

n_values_normal = [n for n, bw in zip(n_values, bw_values) if bw != -1]
bw_values_normal = [bw for bw in bw_values if bw != -1]
alpha_normal = [alpha_values[i] for i, bw in enumerate(bw_values) if bw != -1]
sizes_normal = [sizes[i] for i, bw in enumerate(bw_values) if bw != -1]

# Plotting
plt.figure(figsize=(10, 6))

# Scatter plot for bw where bw == -1 (only if there are entries)
if n_values_beyond_bound:
    plt.scatter(n_values_beyond_bound, bw_values_beyond_bound, color='orange', label='Timed out', marker='o', alpha=alpha_beyond_bound, s=sizes_beyond_bound)

# Scatter plot for bw where bw != -1 (only if there are entries)
if n_values_normal:
    plt.scatter(n_values_normal, bw_values_normal, color='blue', label='bw', marker='o', alpha=alpha_normal, s=sizes_normal)

# Annotate scatter points with counts
for (n, bw), count in count_dict.items():
    plt.text(n - 0.1, bw, str(count), fontsize=9, ha='right', va='center', color='black')

# Line plot for bw_bound
plt.plot(n_values, bw_bound_values, linestyle='--', color='red', label='bw_bound')

# Setting x-axis and y-axis limits and labels
plt.xlabel('Number of vertices (n)')
plt.ylabel('Branch width (bw)')
plt.legend()
plt.grid(True)

# Enforce integer ticks on both axes
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))

# Show plot
plt.show()
