import math

class GFSAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.expanded_nodes = 0
    
    def search(self, start, goal):
        """
        Search for a path from start to goal using Greedy First Search.
        Always chooses the shortest available edge at each step.
        Returns: (path, cost) tuple
        """
        self.expanded_nodes = 0
        
        # Create a copy of the graph structure to avoid modifying original
        available_routes = {}
        for city_from in self.graph:
            for city_to, distance in self.graph[city_from].items():
                available_routes[(city_from, city_to)] = distance
        
        # Create list of all cities we can visit
        remaining_cities = list(self.graph.keys())
        
        # Start building the path
        current_city = start
        path = [start]
        total_distance = 0
        
        # Remove start city from remaining
        if start in remaining_cities:
            remaining_cities.remove(start)
        
        # Greedy search: always pick the shortest edge from current city
        while current_city != goal and remaining_cities:
            cost = math.inf
            next_city = None
            best_route = None
            
            # Find the cheapest route from current city to any remaining city
            for end in remaining_cities:
                route_key = (current_city, end)
                if route_key in available_routes:
                    route_distance = available_routes[route_key]
                    if route_distance > 0 and route_distance < cost:
                        cost = route_distance
                        next_city = end
                        best_route = route_key
            
            # If no valid route found, path doesn't exist
            if next_city is None:
                return (None, 0)
            
            # Move to next city
            path.append(next_city)
            total_distance += cost
            self.expanded_nodes += 1
            
            # Update state
            if best_route in available_routes:
                del available_routes[best_route]
            if next_city in remaining_cities:
                remaining_cities.remove(next_city)
            
            current_city = next_city
            
            # If we reached the goal, return
            if current_city == goal:
                return (path, total_distance)
        
        # Check if we ended at the goal
        if current_city == goal:
            return (path, total_distance)
        
        # No path found
        return (None, 0)