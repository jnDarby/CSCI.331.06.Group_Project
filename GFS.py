import math
import csv

filename = 'data.csv'

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
    
    def add_neighbor(self, neighbor, distance):
        self.neighbors[neighbor] = distance
    
    def get_neighbors(self):
        return self.neighbors.keys()

nodes = {}
allCities = []

with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    allCities = header[0:]
    
    for city in allCities:
        nodes[city] = Node(city)
    
    for row in reader:
        city_from = row[0]
        distances = row[1:]
        
        for city_to, distance_str in zip(allCities, distances):
            distance = float(distance_str)
            nodes[city_from].add_neighbor(nodes[city_to], distance)
            nodes[city_to].add_neighbor(nodes[city_from], distance)

def greedyFirst(startCityName, endCityName=None):
    """Greedy First Search from startCity to endCity (or all cities if endCity=None)"""
    startNode = nodes[startCityName]
    unvisited = set(nodes.values())
    current = startNode
    path = [current.name]
    totalDistance = 0

    unvisited.remove(current)

    while unvisited:
        next_node = None
        min_distance = math.inf
        
        for neighbor, distance in current.neighbors.items():
            if neighbor in unvisited and distance < min_distance:
                min_distance = distance
                next_node = neighbor
        
        if next_node is None:
            break
            
        path.append(next_node.name)
        totalDistance += min_distance
        current = next_node
        unvisited.remove(current)
        
        if endCityName and current.name == endCityName:
            break

    return path, totalDistance

def find_best_starting_city(endCityName=None):
    """Find the best starting city for greedy first (shortest total path)"""
    best_path = None
    best_distance = math.inf
    best_start = None
    
    for startCity in allCities:
        path, distance = greedyFirst(startCity, endCityName)
        if distance < best_distance:
            best_distance = distance
            best_path = path
            best_start = startCity
    
    return best_start, best_path, best_distance

def main():
    print("Available cities:", ", ".join(allCities))
    print("\nEnter starting city (or 'Best' for best starting city):")
    start_input = input().strip()
    
    print("Enter ending city (or leave blank/Enter for full tour):")
    end_input = input().strip()
    
    if start_input.lower() == 'best':
        startCity = None
    else:
        startCity = start_input
        if startCity not in nodes:
            print(f"Invalid starting city: {startCity}")
            return
    
    endCity = end_input if end_input else None
    if endCity and endCity not in nodes:
        print(f"Invalid ending city: {endCity}")
        return
    
    if startCity is None:
        best_start, path, totalDistance = find_best_starting_city(endCity)
        print(f"\nBest starting from: {best_start}")
        print(" -> ".join(path))
        print(f"Total Distance: {totalDistance:.2f} Miles")
    else:
        path, totalDistance = greedyFirst(startCity, endCity)
        print(f"\nPath from {startCity}:")
        print(" -> ".join(path))
        print(f"Total Distance: {totalDistance:.2f} Miles")

if __name__ == "__main__":
    main()
