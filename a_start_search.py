import math
import city_node
from city_node import CityNode

def get_nodes():
    City_Details = city_node.get_All_Nodes()
    allCityNodes = City_Details[0]
    allCities = City_Details[1]
    findShortestAPath(allCityNodes, allCities)

def findShortestAPath(allCityNodes, allCities):
    shortestDistance = math.inf
    current = 0
    shortestPath = ""
    
    for startCity in allCityNodes:
        current = aSearch(startCity, allCities)
        if(current[0] < shortestDistance):
            shortestDistance = current[0]
            shortestPath = current[1]
    print("\nThe shortest path is " + shortestPath + " with a direct line distance of " + str(shortestDistance) + " miles.\n")

def aSearch(startingCity, allCities):
    distance = math.inf
    totalDistance = 0
    path = str(startingCity.name)
    visited = []
    visited.append(startingCity)
    
    while len(visited) < 30: # Calculate h(n_)
        distance = math.inf
        for end in allCities:
            if(end in visited or city_node.get_node_from_name(end) == startingCity):
                None
            else:
                current = startingCity.get_distance(end)
                if(current < distance):
                    distance = current
                    next = end
        visited.append(next)
        totalDistance += distance
        path += " -> " + next

    totalDistance += city_node.get_distance(startingCity, next) # Add g(n)
    totalDistance = round(totalDistance, 3)     # Round to 3 decimal places to find approx f(n)
    return (totalDistance,path)

def main():
    get_nodes()

if __name__ == "__main__":
    main()