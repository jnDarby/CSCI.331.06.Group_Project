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
    
    findStart = input("\nWhat City are you starting from: (Case Sensitive, or 'Best' for best path) ")
    findEnd = input("What City are you going to: (Case Sensitive, or 'Best' for best path) ")
    
    if(findStart != "Best" and findEnd != "Best"):
        for startCity in allCityNodes:
            current = aSearch(startCity, allCities)
            if(current[0] + current[1] < shortestDistance):
                trueDistance = current[0]
                shortestDistance = current[0] + current[1]
                shortestPath = current[2]
    elif(findStart == "Best" and findEnd != "Best"):
        for startCity in allCityNodes:
            if(startCity.name == findEnd):
                None
            else:
                current = aSearch(startCity, allCities)
                if(current[0] + current[1] < shortestDistance):
                    trueDistance = current[0]
                    shortestDistance = current[0] + current[1]
                    shortestPath = current[2]
    elif(findStart != "Best" and findEnd == "Best"):
        for startCity in allCityNodes:
            if(startCity.name == findStart):
                current = aSearch(startCity, allCities)
                if(current[0] + current[1] < shortestDistance):
                    trueDistance = current[0]
                    shortestDistance = current[0] + current[1]
                    shortestPath = current[2]
    else:
        for startCity in allCityNodes:
            current = aSearch(startCity, allCities)
            if(current[0] + current[1] < shortestDistance):
                trueDistance = current[0]
                shortestDistance = current[0] + current[1]
                shortestPath = current[2]
    print("\nThe shortest path is " + shortestPath + " with a direct line distance of " + str(trueDistance) + " miles.\n")

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

    estimate = city_node.get_distance(startingCity, next) # Add g(n)
    totalDistance = round(totalDistance, 3)     # Round to 3 decimal places to find approx f(n)
    return (totalDistance,estimate,path)

def main():
    get_nodes()

if __name__ == "__main__":
    main()