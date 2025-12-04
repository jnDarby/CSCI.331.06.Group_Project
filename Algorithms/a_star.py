import heapq
import math

class AStarAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.expanded_nodes = 0  
        self.coordinates = {}   

    def _heuristic(self, a, b):
        if a not in self.coordinates:
            return 0
        elif b not in self.coordinates:
            return 0
        
        (v, w) = self.coordinates[a]
        (x, y) = self.coordinates[b]
        return math.dist((v, w), (x, y))

    def search(self, start_city, goal_city):
        # Priority queue (f, g, city, path)
        pq = []
        heapq.heappush(pq, (0, 0, start_city, [start_city]))
        visited = {}

        while pq:
            priorityValue, costSoFar, city, path = heapq.heappop(pq)
            self.expanded_nodes += 1
            if city == goal_city:
                return (path, costSoFar)
            #Skip if a better path was found
            if city in visited and visited[city] <= costSoFar:
                continue
            visited[city] = costSoFar
            #Expands neighbors
            for neighbor, cost in self.graph[city].items():
                newCost = costSoFar + cost
                heuristic = self._heuristic(neighbor, goal_city)
                newPrio = newCost + heuristic
                heapq.heappush(pq, (newPrio, newCost, neighbor, path + [neighbor]))

        return None