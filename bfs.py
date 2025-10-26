import csv
from collections import deque

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

def bfs(graph, start, goal):
    traversal =  []
    visited = set()
    queue = deque([start]) #initialize queue with start node
    visited.add(start)

    while queue:
        #traverse through current node
        current_node = queue.popleft() 
        traversal.append(current_node)
        if current_node == goal: 
            return traversal

        #add unvisited neighbors to queue
        for neighbor in graph.get(current_node, []):    
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)


for start_city in allCities:
    for goal_city in allCities:
        message = " from " + start_city + " to " + goal_city + " traversal is: " + str(bfs(graph, 'Rochester', goal_city))
        print(message)

