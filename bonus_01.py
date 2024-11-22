import pandas as pd
import math
import time
import matplotlib.pyplot as plt


def load_and_clean(file_path):
    df = pd.read_csv(file_path, dtype={"Region": str}, low_memory=False)

    relevant_columns = ['Country', 'City', 'Region', 'Latitude', 'Longitude']
    df = df[relevant_columns]
    df = df.dropna(subset=relevant_columns)
    df = df.drop_duplicates(subset=['Latitude', 'Longitude'])
    df['Region'] = df['Region'].astype(str)

    print("Cleaned Dataset Overview:")
    print(df.head())
    print("Null Values:")
    print(df.isnull().sum())
    print(f"Number of rows: {len(df)}")
    return df


def filter_dataset(df, region=None, country=None):
    if region:
        filtered = df[df['Region'] == region]
    elif country:
        filtered = df[df['Country'] == country]
    else:
        filtered = df
    points = list(zip(filtered['Latitude'], filtered['Longitude'], filtered['City']))
    return points


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
    points.sort(key=lambda x: x[0])  # Sort by Latitude (x-coordinate)

    def closest_pair_recursive(points_sorted):
        n = len(points_sorted)
        if n <= 3:
            return closest_pair_brute_force(points_sorted)

        mid = n // 2
        left_half = points_sorted[:mid]
        right_half = points_sorted[mid:]

        d_left, pair_left = closest_pair_recursive(left_half)
        d_right, pair_right = closest_pair_recursive(right_half)

        min_distance = min(d_left, d_right)
        closest_pair = pair_left if d_left <= d_right else pair_right

        mid_x = points_sorted[mid][0]
        in_strip = [p for p in points_sorted if abs(p[0] - mid_x) < min_distance]
        in_strip.sort(key=lambda x: x[1])  # sort by longitude (y-cordnate)

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


def main():
    file_path = 'world_cities.csv'  # Replace with the actual path to your dataset
    df = load_and_clean(file_path)

    subsets = {
        "Specific Region": filter_dataset(df, region="06"),  # any region code works here
        "Specific Country": filter_dataset(df, country="ad"),  # any country code as well nw
        "Entire Dataset": filter_dataset(df)
    }

    results = {}

    for subset_name, points in subsets.items():
        print(f"Processing subset: {subset_name} ({len(points)} points)")

        # Time for brute force
        start_time = time.time()
        min_distance_bf, closest_pair_bf = closest_pair_brute_force(points)
        end_time = time.time()
        bf_time = end_time - start_time

        # Time for divide-and-conquer
        start_time = time.time()
        min_distance_dc, closest_pair_dc = closest_pair_divide_and_conquer(points)
        end_time = time.time()
        dc_time = end_time - start_time

        # Store results
        results[subset_name] = {
            "Brute Force": {
                "Closest Pair": closest_pair_bf,
                "Minimum Distance": min_distance_bf,
                "Runtime": bf_time
            },
            "Divide and Conquer": {
                "Closest Pair": closest_pair_dc,
                "Minimum Distance": min_distance_dc,
                "Runtime": dc_time
            }
        }

        print(f"Brute Force: {results[subset_name]['Brute Force']}")
        print(f"Divide and Conquer: {results[subset_name]['Divide and Conquer']}\n")

    subset_names = list(results.keys())
    bf_runtimes = [results[name]["Brute Force"]["Runtime"] for name in subset_names]
    dc_runtimes = [results[name]["Divide and Conquer"]["Runtime"] for name in subset_names]

    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    x = range(len(subset_names))

    plt.bar(x, bf_runtimes, bar_width, label='Brute Force', alpha=0.7)
    plt.bar([p + bar_width for p in x], dc_runtimes, bar_width, label='Divide and Conquer', alpha=0.7)

    plt.xlabel("Dataset Subsets")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime Comparison for Different Dataset Subsets")
    plt.xticks([p + bar_width / 2 for p in x], subset_names, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('bonus_01.png')


if __name__ == "__main__":
    main()