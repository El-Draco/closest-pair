import random
import time
import matplotlib.pyplot as plt
import math


# Function to generate random points
def generate_points(n):
    return [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]


# Helper function to calculate Euclidean distance
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# Brute-force approach
def closest_pair_brute_force(points):
    min_distance = float('inf')
    closest_pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            distance = euclidean_distance(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = (points[i], points[j])
    return min_distance, closest_pair


# Divide-and-conquer approach
def closest_pair_divide_and_conquer(points):
    points.sort(key=lambda x: x[0])  # Sort points by x-coordinate

    def closest_pair_recursive(points_sorted):
        n = len(points_sorted)
        if n <= 3:  # Use brute-force for small sizes
            return closest_pair_brute_force(points_sorted)

        mid = n // 2
        left_half = points_sorted[:mid]
        right_half = points_sorted[mid:]

        d_left, pair_left = closest_pair_recursive(left_half)
        d_right, pair_right = closest_pair_recursive(right_half)

        min_distance = min(d_left, d_right)
        closest_pair = pair_left if d_left <= d_right else pair_right

        # Check points near the dividing line
        mid_x = points_sorted[mid][0]
        in_strip = [p for p in points_sorted if abs(p[0] - mid_x) < min_distance]
        in_strip.sort(key=lambda x: x[1])  # Sort by y-coordinate

        for i in range(len(in_strip)):
            for j in range(i + 1, len(in_strip)):
                if (in_strip[j][1] - in_strip[i][1]) >= min_distance:
                    break
                distance = euclidean_distance(in_strip[i], in_strip[j])
                if distance < min_distance:
                    min_distance = distance
                    closest_pair = (in_strip[i], in_strip[j])

        return min_distance, closest_pair

    return closest_pair_recursive(points)


# Main script
dataset_sizes = [100, 500, 1000, 10000, 100000]
brute_force_times = []
divide_and_conquer_times = []

for n in dataset_sizes:
    points = generate_points(n)

    # Time for brute force
    start_time = time.time()
    closest_pair_brute_force(points)
    end_time = time.time()
    brute_force_times.append(end_time - start_time)

    # Time for divide-and-conquer
    start_time = time.time()
    closest_pair_divide_and_conquer(points)
    end_time = time.time()
    divide_and_conquer_times.append(end_time - start_time)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(dataset_sizes, brute_force_times, marker='o', label="Brute Force")
plt.plot(dataset_sizes, divide_and_conquer_times, marker='o', label="Divide and Conquer")
plt.xlabel("Dataset Size (n)")
plt.ylabel("Runtime (seconds)")
plt.title("Performance of Closest Pair Algorithms")
plt.legend()
plt.grid()
plt.savefig('results.png')
plt.show()

# Time complexity theoretical comparison
print("Dataset Sizes:", dataset_sizes)
print("Brute Force Times:", brute_force_times)
print("Divide and Conquer Times:", divide_and_conquer_times)
