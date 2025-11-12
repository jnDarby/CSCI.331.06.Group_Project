import csv
import time
import heapq

filename = 'data.csv'
allCities = []
graph = {}

with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    allCities = header[0:]
  
    for row in reader:
        cityFrom = row[0]
        distances = row[1:]
        graph[cityFrom] = {}

        for cityTo, distance_str in zip(allCities, distances):
            distance = float(distance_str)
            graph[cityFrom][cityTo] = distance

    print("Graph loaded successfully")

def ucs(graph, start, goal):
    startTime = time.perf_counter()
    frontier = [(0, start, [start])]  # (cost, current_city, path)
    visited = set()
    expanded_nodes = 0

    while frontier:
        cost, city, path = heapq.heappop(frontier)

        if city in visited:
            continue
        visited.add(city)
        expanded_nodes += 1

        if city == goal:
            endTime = time.perf_counter()
            return {
                'start': start,
                'goal': goal,
                'path': path,
                'total_cost': cost,
                'expanded_nodes': expanded_nodes,
                'time': round(endTime - startTime, 6)
            }

        for neighbor, distance in graph[city].items():
            if neighbor not in visited and distance >= 0:
                heapq.heappush(frontier, (cost + distance, neighbor, path + [neighbor]))

    endTime = time.perf_counter()
    return {
        'start': start,
        'goal': goal,
        'path': None,
        'total_cost': float('inf'),
        'expanded_nodes': expanded_nodes,
        'time': round(endTime - startTime, 6)
    }


for start_city in allCities:
    for goal_city in allCities:
        result = ucs(graph, start_city, goal_city)
        print(f"{result['start']} → {result['goal']} | "
              f"Cost: {result['total_cost']} | "
              f"Expanded: {result['expanded_nodes']} | "
              f"Time: {result['time']}s | "
              f"Path: {result['path']}")