import random
import math
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate the total distance of a given route
def calculate_total_distance(distances, route):
    total_distance = 0
    for i in range(len(route)):
        start_city = route[i]
        if i == len(route) - 1:
            end_city = route[0]  # Go back to the starting city
        else:
            end_city = route[i + 1]
        total_distance += distances[start_city][end_city]
    return total_distance

# Function to generate a random initial route
def generate_initial_route(num_cities):
    route = list(range(num_cities))
    random.shuffle(route)
    return route

# Function to explore neighboring solutions
def explore_neighbors(route):
    neighbors = []
    for i in range(len(route)):
        for j in range(i + 1, len(route)):
            neighbor = route.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

# Hill climbing algorithm
def hill_climbing(distances, max_iterations=1000):
    num_cities = len(distances)
    current_route = generate_initial_route(num_cities)
    current_distance = calculate_total_distance(distances, current_route)
    best_route = current_route
    best_distance = current_distance

    iterations = 0
    while iterations < max_iterations:
        neighbors = explore_neighbors(current_route)
        best_neighbor = None
        best_neighbor_distance = float('inf')

        for neighbor in neighbors:
            neighbor_distance = calculate_total_distance(distances, neighbor)
            if neighbor_distance < best_neighbor_distance:
                best_neighbor = neighbor
                best_neighbor_distance = neighbor_distance

        if best_neighbor_distance < current_distance:
            current_route = best_neighbor
            current_distance = best_neighbor_distance
            best_route = current_route
            best_distance = current_distance
        else:
            break  # No improving neighbor found, reached a local optimum

        iterations += 1

    return best_route, best_distance

# Visualization function
def visualize_navigation(distances, route, city_names=None, city_coords=None):
    num_cities = len(distances)

    if city_coords is None:
        city_coords = np.random.rand(num_cities, 2)

    if city_names is None:
        city_names = [str(i) for i in range(num_cities)]

    plt.figure(figsize=(8, 8))
    plt.scatter(city_coords[:, 0], city_coords[:, 1], s=200, color='blue')
    plt.plot(city_coords[route, 0], city_coords[route, 1], 'ro--')
    for i, city in enumerate(city_names):
        plt.annotate(city, (city_coords[i, 0], city_coords[i, 1]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.title("Robot Navigation Optimization")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.show()

# Example usage
distances = [
    [0, 7, 20, 15, 12],
    [7, 0, 6, 14, 18],
    [20, 6, 0, 15, 30],
    [15, 14, 15, 0, 2],
    [12, 18, 30, 2, 0]
]

city_names = ['Dorado Park', 'Khomasdal', 'Katutura', 'Eros', 'Klein Windhoek']
city_coords = np.array([[1, 2], [30, 21], [56, 23], [8, 18], [20, 50]])

best_route, best_distance = hill_climbing(distances)
print("Best Route:", [city_names[i] for i in best_route])
print("Total Distance:", best_distance)

visualize_navigation(distances, best_route, city_names, city_coords)
