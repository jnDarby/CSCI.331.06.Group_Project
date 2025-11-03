import math
import csv
import time

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
            cityFrom = row[0]# its the first cell in the city name
            distances = row[1:] # rest are the distances

            # now creating a dictionary for this city's neighbors
            graph[cityFrom] = {}

            for cityTo, distance_str in zip(allCities, distances):
                distance = float(distance_str)
                if distance > 0: # only add if theres an actual route between the two
                    graph[cityFrom][cityTo] = distance


    print("Graph Loaded Successfully!")
    print(f"Rochesters Neighbors: {graph['Rochester']}") # all neighbors of rochester


def dfsAlgoRecursive(graph, current, goal, path, cost, expanded_nodes):
    path.append(current)
    expanded_nodes[0] += 1

    # print(f"Exploring: {current}, Path so far: {' -> '.join(path)}")

    if current == goal:
        return (path.copy(), cost)
    
    # recursive path
    neighbors = sorted(graph.get(current, {}).keys())

    for neighbor in neighbors:
        if neighbor not in path:
            edge_cost = graph[current][neighbor]
            result, total_cost = dfsAlgoRecursive(graph, neighbor, goal, path, cost + edge_cost, expanded_nodes)
            if result:
                return (result, total_cost)
            
    # now backtrack if the path doesnt work 
    path.pop()
    # visited.remove(current)
    return (None, 0)

start = 'Rochester'
allCities = list(graph.keys())

print("="*75)
print(f"Route Planner - Starting from {start}")
print("="*75)
print(f"{'Destination':<20} {'Distance (mi)':<15} {'Stops':<10} {'Expanded':<12} {'Time (ms)'}")
print("-"*75)

allResults = []

for goal in allCities:
    if goal == start:
        continue

    # visitedCities = set()
    path = []
    expandedNodes = [0]
    

    startTime = time.time()
    resultPath, totalDistance = dfsAlgoRecursive(graph, start, goal, path, 0, expandedNodes)
    endTime = time.time()
    runtime = (endTime - startTime) * 1000

    if resultPath:
        numberOfStops = len(resultPath) - 1
        print(f"{goal:<20} {totalDistance:<15.2f} {numberOfStops:<10} {expandedNodes[0]:<12} {runtime:<.4f}")
        allResults.append({
            'destination': goal,
            'distance': totalDistance,
            'stops': numberOfStops,
            'expanded': expandedNodes[0],
            'runtime': runtime,
            'path': resultPath
        })
    else:
        print(f"{goal:<20} {'No path found':<15} {'-':<10}")

print("="*80)
print()

print("="*80)
print("Detailed Results")
print("="*80)

for i, result in enumerate(allResults):
    print(f"\n{'='*80}")
    print(f"Route to: {result['destination']}")
    print(f"{'='*80}")
    print(f"Path: {' --> '.join(result['path'])}")

    # show each step as well
    print("\nStep by Step Breakdown:")
    for j in range(len(result['path']) - 1):
        cityFrom = result['path'][j]
        cityTo = result['path'][j+1]
        distance = graph[cityFrom][cityTo]
        print(f" {j+1}. {cityFrom} --> {cityTo}: {distance:.2f} miles")
    print(f"\n  TOTAL DISTANCE: {result['distance']:.2f} miles")
    print(f"\n  Number of Stops: {result['stops']}")
    print(f"\n  Nodes Explored: {result['expanded']}")
    print(f"\n  Runtime: {result['runtime']:.4f} ms")

print("\n" + "="*80)

# summary of the stats
if allResults:
    averageDistance = sum(r['distance'] for r in allResults) / len(allResults)
    averageStops = sum(r['stops'] for r in allResults) / len(allResults)
    averageExpanded = sum(r['expanded'] for r in allResults) / len(allResults)