import math
import csv

class IDAAlgorithm:
    def __init__(self, actualGraph, estimateGraph=None):
        self.graph = actualGraph
        self.heuristicValues = estimateGraph
        self.expanded_nodes = 0
    
    def search(self, start, goal):
        """
        Search for a path from start to goal using IDA*.
        Returns: (path, cost) tuple
        """
        self.expanded_nodes = 0
        bound = self._heuristic(start, goal)
        path = [start]
        
        while True:
            t, found_cost, found_path = self._ida_search(path, 0, bound, goal)
            if t == "FOUND":
                return found_path, found_cost
            if t == math.inf:
                return None, 0
            bound = t
    
    def _heuristic(self, current_city, goal_city):
        """Heuristic function - estimate from current to goal"""
        return self.heuristicValues.get(current_city, {}).get(goal_city, 0)
    
    def _ida_search(self, path, g, bound, goalCity):
        current_city = path[-1]
        self.expanded_nodes += 1
        
        f = g + self._heuristic(current_city, goalCity)
        if f > bound:
            return f, None, None
        if current_city == goalCity:
            return "FOUND", g, list(path)

        min_excess = math.inf
        
        for neighbor, cost in self.graph.get(current_city, {}).items():
            if neighbor in path:  
                continue
            path.append(neighbor)
            t, found_cost, found_path = self._ida_search(path, g + cost, bound, goalCity)
            path.pop()
            
            if t == "FOUND":
                return "FOUND", found_cost, found_path
            if isinstance(t, (int, float)) and t < min_excess:
                min_excess = t
        
        return min_excess, None, None