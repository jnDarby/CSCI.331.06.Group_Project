import math
import csv

filename = 'data.csv'

allCities = []
graph = {}

with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # read the header row with city names
    allCities = header[0:]  # skip the first empty cell adn get the city names next 

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        allCities = header[0:]

        for row in reader:
            city_from = row[0]# its the first cell in the city name
            distances = row[1:] # rest are the distances

            # now creating a dictionary for this city's neighbors
            graph[city_from] = {}

            for city_to, distance_str in zip(allCities, distances):
                distance = float(distance_str)
                if distance > 0: # only add if theres an actual route between the two
                    graph[city_from][city_to] = distance


    print("Graph Loaded Successfully!")
    print(f"Rochesters Neighbors: {graph['Rochester']}") # all neighbors of rochester


def dfsAlgoRecursive(graph, current, goal, visited, path, cost):
    path.append(current)
    visited.add(current)

    if current == goal:
        return (path.copy(), cost)
    
    # recursive path
    for neighbor in graph.get(current, {}):
        if neighbor not in visited:
            edge_cost = graph[current][neighbor]
            result, total_cost = dfsAlgoRecursive(graph, neighbor, goal, visited, path, cost + edge_cost)
            if result:
                return (result, total_cost)
            
    # now backtrack if the path doesnt work 
    path.pop()
    return (None, 0)

print("Cities in the Graph: ", list(graph.keys())[:5])

start = 'Rochester'
goal = 'New York City'
visited_cities = set()
path = []

print("Recursive DFS Traversal: ")
result = dfsAlgoRecursive(graph, start, goal, visited_cities, path, 0)
print(result)
