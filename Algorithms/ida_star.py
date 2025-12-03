import math
import csv

class CityNode:
    def __init__(self, name):
        self.name = name
        self.distances = {}  # Dictionary to hold cities and distances
        
    def __str__(self):
        return self.name
    
    def add_distance(self, city, distance):
        self.distances[city] = distance
        
    def get_distance(self, city):
        return self.distances.get(city, float('inf'))


class IDAAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.expanded_nodes = 0
        self.allCityNodes = []
        self.allCities = list(graph.keys())
        self._create_city_nodes()
    
    def _create_city_nodes(self):
        """Convert graph dictionary to CityNode objects"""
        for city_name in self.allCities:
            node = CityNode(city_name)
            for neighbor, distance in self.graph[city_name].items():
                node.add_distance(neighbor, distance)
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
        if not startCity:
            return (None, 0)
        
        dist, path_str = self._ida_search_start(startCity)
        
        if path_str:
            path = path_str.split(" -> ")
            return (path, dist)
        return (None, 0)
    
    def _heuristic(self, current_city, start_city):
        """Heuristic function"""
        return current_city.get_distance(start_city.name)
    
    def _ida_search_start(self, startCity):
        """IDA* main search loop"""
        bound = self._heuristic(startCity, startCity)
        path = [startCity]
        best_cost = math.inf
        best_path_str = startCity.name

        while True:
            t, found_cost, found_path_str = self._search_ida(
                path=path,
                g=0.0,
                bound=bound,
                startCity=startCity
            )

            if t == "FOUND":
                return found_cost, found_path_str

            if t == math.inf:
                return best_cost, best_path_str

            bound = t
    
    def _search_ida(self, path, g, bound, startCity):
        """Recursive IDA* search"""
        current_city = path[-1]
        self.expanded_nodes += 1

        if len(path) == len(self.allCityNodes):
            path_str = " -> ".join(city.name for city in path)
            return "FOUND", g, path_str

        f = g + self._heuristic(current_city, startCity)
        if f > bound:
            return f, None, None

        min_excess = math.inf

        for end_name in self.allCities:
            next_node = self._get_node_from_name(end_name)
            if next_node in path:
                continue

            cost = current_city.get_distance(end_name)
            new_g = g + cost

            path.append(next_node)
            t, found_cost, found_path_str = self._search_ida(
                path, new_g, bound, startCity
            )
            path.pop()

            if t == "FOUND":
                return "FOUND", found_cost, found_path_str

            if isinstance(t, (int, float)) and t < min_excess:
                min_excess = t

        return min_excess, None, None


# Standalone usage
if __name__ == "__main__":
    filename = 'data.csv'
    allCities = []
    graph = {}
    
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        allCities = header[1:]
        
        for row in reader:
            city_from = row[0]
            distances = row[1:]
            graph[city_from] = {}
            
            for city_to, distance_str in zip(allCities, distances):
                distance = float(distance_str)
                if distance > 0:
                    graph[city_from][city_to] = distance
    
    print("Graph loaded successfully")
    
    ida = IDAAlgorithm(graph)
    start = 'Rochester'
    goal = 'New York City'
    path, cost = ida.search(start, goal)
    
    if path:
        print(f"\nPath from {start} to {goal}:")
        print(f"Route: {' -> '.join(path)}")
        print(f"Total Distance: {cost} miles")
        print(f"Nodes Expanded: {ida.expanded_nodes}")
    else:
        print(f"No path found from {start} to {goal}")