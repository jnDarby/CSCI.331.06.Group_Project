import csv
from collections import deque
import time

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
    startTime = time.perf_counter()
    nodes_expanded = 1
    traversal =  []
    visited = set()
    queue = deque([start]) #initialize queue with start node
    visited.add(start)

    while queue:
        #traverse through current node
        current_node = queue.popleft() 
        traversal.append(current_node)
        if current_node == goal: 
            endTime = time.perf_counter()
            runtime = endTime - startTime
            message =  " from " + start_city + " to " + goal_city + " runtime is:" + str(runtime) + ", nodes expanded is:" + str(nodes_expanded) + ", traversal is: " + str(traversal)
            return message

        #add unvisited neighbors to queue
        for neighbor in graph.get(current_node, {}):    
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
        
        nodes_expanded += 1
 

for start_city in allCities:
    for goal_city in allCities:
       print(bfs(graph, start_city, goal_city))


