import random
import math
import time
import matplotlib.pyplot as plt
import bisect


# Generate random 2D points
def generate_points(n, range_min=0, range_max=1000000):
    points = set()
    while len(points) < n:
        x = random.uniform(range_min, range_max)
        y = random.uniform(range_min, range_max)
        points.add((x, y))
    return list(points)


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def closest_pair_sweep_line(points):
    #sort by x first
    points.sort(key=lambda x: x[0])

    # active set (sorted by y-coordinate)
    active_set = []
    min_distance = float('inf')
    closest_pair = None

    for i, point in enumerate(points):
        # Remov points from the active set that are too far along x
        while active_set and (point[0] - active_set[0][0] > min_distance):
            active_set.pop(0)

        bisect.insort(active_set, point)

        for j in range(len(active_set) - 1, -1, -1):
            if abs(active_set[j][1] - point[1]) >= min_distance:
                break
            if active_set[j] != point:
                distance = euclidean_distance(point, active_set[j])
                if distance < min_distance:
                    min_distance = distance
                    closest_pair = (point, active_set[j])

    return min_distance, closest_pair

def main():
    dataset_sizes = [100, 500, 1000, 10000, 100000, 1000000]  # Increasing dataset sizes
    runtimes = []

    for n in dataset_sizes:
        points = generate_points(n)

        start_time = time.time()
        min_distance, closest_pair = closest_pair_sweep_line(points)
        end_time = time.time()

        runtime = end_time - start_time
        runtimes.append(runtime)

        print(f"Dataset Size: {n}")
        print(f"Closest Pair: {closest_pair}")
        print(f"Minimum Distance: {min_distance:.6f}")
        print(f"Runtime: {runtime:.6f} seconds\n")

    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, runtimes, marker='o', label='Sweep Line Algorithm')
    plt.xlabel("Dataset Size (n)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Performance of Sweep Line Algorithm")
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    plt.legend()
    plt.savefig('bonus_02.png')

    # Theoretical complexity comparison
    print("Theoretical Complexity: O(n log n)")
    print("Experimental Runtimes:", runtimes)


if __name__ == "__main__":
    main()
