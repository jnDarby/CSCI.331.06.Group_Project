import csv
import time

filename = 'data.csv'

allCities = []
graph = {}

# Load the graph from CSV
try:
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        # Read all lines first to debug
        lines = list(reader)
        
        if not lines:
            print("ERROR: CSV file is empty!")
            exit(1)
        
        # First line is the header with city names
        header = lines[0]
        allCities = header
        
        print(f"Found {len(allCities)} cities in header")
        
        # Remaining lines are the distance data
        for row in lines[1:]:
            if not row or len(row) == 0:
                continue
                
            cityFrom = row[0]  # First column is the source city
            distances = row[1:]  # Rest are distances
            
            graph[cityFrom] = {}
            
            for cityTo, distance_str in zip(allCities, distances):
                try:
                    distance = float(distance_str)
                    if distance > 0:  # Only add if there's an actual connection
                        graph[cityFrom][cityTo] = distance
                except ValueError:
                    continue
                    
except FileNotFoundError:
    print(f"ERROR: Could not find file '{filename}'")
    print("Make sure data.csv is in the same directory as ids.py")
    exit(1)
except Exception as e:
    print(f"ERROR loading CSV: {e}")
    exit(1)

print("Graph Loaded Successfully!")
print(f"Rochester's Neighbors: {graph['Rochester']}")

def dls(graph, current, goal, depth_limit, path, cost, expanded_nodes):
    """Depth-Limited Search helper function for IDS"""
    expanded_nodes[0] += 1
    
    # Goal found
    if current == goal:
        return (path + [current], cost)
    
    # Depth limit reached
    if depth_limit == 0:
        return (None, 0)
    
    # Explore neighbors in sorted order
    neighbors = sorted(graph.get(current, {}).keys())
    
    for neighbor in neighbors:
        if neighbor not in path:
            edge_cost = graph[current][neighbor]
            result, total_cost = dls(
                graph, 
                neighbor, 
                goal, 
                depth_limit - 1, 
                path + [current], 
                cost + edge_cost, 
                expanded_nodes
            )
            if result:
                return (result, total_cost)
    
    return (None, 0)

def idsAlgo(graph, start, goal, max_depth=50):
    """Iterative Deepening Search Algorithm"""
    expanded_nodes = [0]
    
    for depth in range(max_depth):
        path = []
        result, total_cost = dls(graph, start, goal, depth, path, 0, expanded_nodes)
        
        if result:
            return (result, total_cost, expanded_nodes[0])
    
    return (None, 0, expanded_nodes[0])

start = 'Rochester'
allCities = list(graph.keys())

print("="*75)
print(f"Route Planner - Starting from {start} (Using IDS)")
print("="*75)
print(f"{'Destination':<20} {'Distance (mi)':<15} {'Stops':<10} {'Expanded':<12} {'Time (ms)'}")
print("-"*75)

allResults = []

for goal in allCities:
    if goal == start:
        continue
    
    startTime = time.time()
    resultPath, totalDistance, expandedNodes = idsAlgo(graph, start, goal)
    endTime = time.time()
    runtime = (endTime - startTime) * 1000
    
    if resultPath:
        numberOfStops = len(resultPath) - 1
        print(f"{goal:<20} {totalDistance:<15.2f} {numberOfStops:<10} {expandedNodes:<12} {runtime:<.4f}")
        allResults.append({
            'destination': goal,
            'distance': totalDistance,
            'stops': numberOfStops,
            'expanded': expandedNodes,
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

# Summary statistics
if allResults:
    averageDistance = sum(r['distance'] for r in allResults) / len(allResults)
    averageStops = sum(r['stops'] for r in allResults) / len(allResults)
    averageExpanded = sum(r['expanded'] for r in allResults) / len(allResults)
    averageRuntime = sum(r['runtime'] for r in allResults) / len(allResults)
    
    print("\nSUMMARY STATISTICS (IDS Algorithm)")
    print("="*80)
    print(f"Average Distance: {averageDistance:.2f} miles")
    print(f"Average Stops: {averageStops:.2f}")
    print(f"Average Nodes Expanded: {averageExpanded:.2f}")
    print(f"Average Runtime: {averageRuntime:.4f} ms")
    print("="*80)