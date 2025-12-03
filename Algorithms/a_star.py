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


class AStarAlgorithm:
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
    
    def _get_distance(self, city_from, city_to):
        """Get distance between two city nodes"""
        return city_from.get_distance(city_to)
    
    def search(self, start, goal):
        """
        Search for a path from start to goal using A* Search.
        Returns: (path, cost) tuple
        """
        self.expanded_nodes = 0
        
        startCity = self._get_node_from_name(start)
        if not startCity:
            return (None, 0)
        
        result = self._aSearch(startCity)
        totalDistance = result[0]
        estimate = result[1]
        path_str = result[2]
        
        if path_str:
            path = path_str.split(" -> ")
            # Return actual traveled distance (not f(n))
            return (path, totalDistance)
        return (None, 0)
    
    def _aSearch(self, startingCity):
        """A* Search implementation - original approach"""
        distance = math.inf
        totalDistance = 0
        path = str(startingCity.name)
        visited = []
        visited.append(startingCity)
        
        # Calculate h(n) - visit all cities greedily
        while len(visited) < len(self.allCityNodes):
            distance = math.inf
            next_city = None
            
            for end in self.allCities:
                end_node = self._get_node_from_name(end)
                if end_node in visited or end_node == startingCity:
                    continue
                else:
                    current = startingCity.get_distance(end)
                    if current < distance:
                        distance = current
                        next_city = end
            
            if next_city is None:
                break
                
            next_node = self._get_node_from_name(next_city)
            visited.append(next_node)
            self.expanded_nodes += 1
            totalDistance += distance
            path += " -> " + next_city
            startingCity = next_node
        
        # Add g(n) - estimate to goal
        estimate = self._get_distance(startingCity, visited[0])
        totalDistance = round(totalDistance, 3)  # Round to 3 decimal places to find approx f(n)
        
        return (totalDistance, estimate, path)


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
    
    astar = AStarAlgorithm(graph)
    start = 'Rochester'
    goal = 'New York City'
    path, cost = astar.search(start, goal)
    
    if path:
        print(f"\nPath from {start} to {goal}:")
        print(f"Route: {' -> '.join(path)}")
        print(f"Total Distance: {cost} miles")
        print(f"Nodes Expanded: {astar.expanded_nodes}")
    else:
        print(f"No path found from {start} to {goal}")