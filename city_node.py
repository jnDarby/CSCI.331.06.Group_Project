import csv

allCityNodes = []

def get_All_Nodes():
    filename = 'data.csv'
    
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read the header row with city names
        allCities = header[0:]  # Store values
        for row in reader:
            city_from = row[0]  # first cell in the row is the city name            
            distances = row[1:]
            
            city_node = create_city_node(city_from)
                
            for city_to, distance_str in zip(allCities, distances):
                distance = float(distance_str)
                city_node.add_distance(city_to, distance)
                
            allCityNodes.append(city_node)
                
    return allCityNodes, allCities

def get_distance(city_from, city_to):
    return city_from.get_distance(city_to)

def get_node_from_name(name):
    for node in allCityNodes:
        if node.name == name:
            return node
    return None

def create_city_node(name, distances={}):
    node = CityNode(name)
    for city, distance in distances.items():
        node.add_distance(city, distance)
    return node

def get_name_from_node(node):
    return node.name

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