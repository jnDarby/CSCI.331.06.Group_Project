import heapq

class AStarAlgorithm:
    def __init__(self, actualGraph, estimateGraph):
        self.graph = actualGraph
        self.heuristicValues = estimateGraph
        self.expanded_nodes = 0  

    def search(self, start_city, goal_city):
        if start_city == goal_city:
            return ([start_city], 0)
            
        priorityq = []
        heapq.heappush(priorityq, (0, 0, start_city))  # (f, g, node)
        cameFrom = {}
        costSoFar = {start_city: 0}
        
        while priorityq:
            _, currentCost, current = heapq.heappop(priorityq)
            
            if current in costSoFar and currentCost > costSoFar[current]:
                continue
                
            self.expanded_nodes += 1
            if current == goal_city:
                path = []
                total = current
                while total in cameFrom:
                    path.append(total)
                    total = cameFrom[total]
                path.append(start_city)
                return (path[::-1], costSoFar[current])
            
            for neighbor, cost in self.graph[current].items():
                newCost = costSoFar[current] + cost
                t = costSoFar.get(neighbor, float('inf'))
                if (newCost < t):
                    costSoFar[neighbor] = newCost
                    heuristic = self.heuristicValues[neighbor][current]
                    priority = newCost + heuristic
                    heapq.heappush(priorityq, (priority, newCost, neighbor))
                    cameFrom[neighbor] = current
        
        return None
