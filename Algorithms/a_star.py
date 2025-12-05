import heapq
import math

class AStarAlgorithm:
    def __init__(self, actualGraph, estimateGraph):
        self.graph = actualGraph
        self.heuristicValues = estimateGraph
        self.expanded_nodes = 0  
        self.coordinates = {}   

    def search(self, start_city, goal_city):
        priorityq = []
        heapq.heappush(priorityq, (0, 0, start_city, [start_city]))
        visited = {}

        while priorityq:
            priorityValue, costSoFar, city, path = heapq.heappop(priorityq)
            self.expanded_nodes += 1
            if city == goal_city:
                return (path, costSoFar)
            #Skip if a better path was found
            if city in visited and visited[city] <= costSoFar:
                continue
            visited[city] = costSoFar
            #Expands neighbors
            for neighbor, cost in self.graph[city].items():
                if( neighbor not in path):
                    newCost = costSoFar + cost
                    heuristic = self.heuristicValues[neighbor][start_city]
                    newPrio = newCost + heuristic
                    heapq.heappush(priorityq, (newPrio, newCost, neighbor, path + [neighbor]))

        print(priorityq)
        return None