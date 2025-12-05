import math
import csv

class CityNode:
    def __init__(self, name):
        self.name = name
        self.distances = {}  # Dictionary to hold cities and distances
        self.estimates = {}  # Dictionary to hold cities and estimates
        
    def __str__(self):
        return self.name
        
    def add_distance(self, city, distance, estimate):
        self.distances[city] = distance
        self.estimates[city] = estimate
        
    def get_distance(self, city):
        return self.distances.get(city, float('inf'))
    
    def get_estimate(self, city):
        return self.estimates.get(city, float('inf'))

class IDAAlgorithm:
    def __init__(self, actualGraph, estimateGraph=None):
        self.graph = actualGraph
        self.heuristicValues = estimateGraph or actualGraph  # Default to actualGraph if no estimateGraph
        self.expanded_nodes = 0
        self.allCityNodes = []
        self.allCities = list(actualGraph.keys())
        self._create_city_nodes()
    
    def _create_city_nodes(self):
        """Convert graph dictionary to CityNode objects"""
        for city_name in self.allCities:
            node = CityNode(city_name)
            for neighbor, distance in self.graph[city_name].items():
                # Use actual distance for heuristic if estimate not available
                estimate = self.heuristicValues[city_name].get(neighbor, distance)
                node.add_distance(neighbor, distance, estimate)
            self.allCityNodes.append(node)
    
    def _get_node_from_name(self, name):
        """Get CityNode from city name"""
        for node in self.allCityNodes:
            if node.name == name:
                return node
        return None
    
    def search(self, start, goal):
        """
        Search for a path from start to goal using IDA*.
        Returns: (path, cost) tuple
        """
        self.expanded_nodes = 0
        
        startCity = self._get_node_from_name(start)
        goalCity = self._get_node_from_name(goal)
        if not startCity or not goalCity:
            return (None, 0)
        
        dist, path_str = self._ida_search_start(startCity, goalCity)
        
        if path_str:
            path = path_str.split(" -> ")
            return (path, dist)
        return (None, 0)
    
    def _heuristic(self, current_city, goal_city):
        """Heuristic function - estimate from current to goal"""
        return current_city.get_estimate(goal_city.name)
    
    def _ida_search_start(self, startCity, goalCity):
        """IDA* main search loop"""
        bound = self._heuristic(startCity, goalCity)
        path = [startCity]
        
        while True:
            t, found_cost, found_path_str = self._search_ida(
                path=path,
                g=0.0,
                bound=bound,
                goalCity=goalCity
            )
            
            if t == "FOUND":
                return found_cost, found_path_str
            
            if t == math.inf:
                return math.inf, None
            
            bound = t
    
    def _search_ida(self, path, g, bound, goalCity):
        """Recursive IDA* search"""
        current_city = path[-1]
        self.expanded_nodes += 1
        
        # Check goal condition
        if current_city.name == goalCity.name:
            path_str = " -> ".join(city.name for city in path)
            return "FOUND", g, path_str
        
        f = g + self._heuristic(current_city, goalCity)
        if f > bound:
            return f, None, None
        
        min_excess = math.inf
        
        # Only iterate over actual neighbors (not all cities)
        for end_name in current_city.distances:
            next_node = self._get_node_from_name(end_name)
            if next_node in path:
                continue
            
            cost = current_city.get_distance(end_name)
            if cost == float('inf'):
                continue
            new_g = g + cost
            
            path.append(next_node)
            t, found_cost, found_path_str = self._search_ida(
                path, new_g, bound, goalCity
            )
            path.pop()
            
            if t == "FOUND":
                return "FOUND", found_cost, found_path_str
            
            if isinstance(t, (int, float)) and t < min_excess:
                min_excess = t
        
        return min_excess, None, None