import math
import city_node
from city_node import CityNode


def get_nodes():
    City_Details = city_node.get_All_Nodes()
    allCityNodes = City_Details[0]
    allCities = City_Details[1]
    findShortestIDAPath(allCityNodes, allCities)


def findShortestIDAPath(allCityNodes, allCities):
    findStart = input("Enter starting city (or enter 'Best' to search from all cities): ")
    findEnd = input("Enter ending city (or enter 'Best' to search to all cities): ")

    if findStart == "Best" and findEnd == "Best":
        distances = findTotalShortest(allCityNodes, allCities)
        shortestDistance, shortestPath, trueDistance = distances
    elif findStart != "Best" and findEnd == "Best":
        distances = findBestWhereStart(allCityNodes, allCities, findStart)
        shortestDistance, shortestPath, trueDistance = distances
    elif findStart == "Best" and findEnd != "Best":
        distances = findBestWhereEnd(allCityNodes, allCities, findEnd)
        shortestDistance, shortestPath, trueDistance = distances
    else:
        distances = findBestWhereBoth(allCityNodes, allCities, findStart, findEnd)
        shortestDistance, shortestPath, trueDistance = distances

    print("\nThe shortest path is " + shortestPath + 
          " with a direct line distance of " + str(trueDistance) + " miles.\n")
    
def findBestWhereBoth(allCityNodes, allCities, findStart, findEnd):
    shortestDistance = math.inf
    shortestPath = ""
    trueDistance = math.inf
    
    startCity = city_node.get_node_from_name(findStart)
    endCity = city_node.get_node_from_name(findEnd)
    dist, path = ida_search_start(startCity, allCityNodes, allCities)
    if dist < shortestDistance:
        shortestDistance = dist
        trueDistance = dist
        shortestPath = path
    return shortestDistance, shortestPath, trueDistance
    
def findBestWhereEnd(allCityNodes, allCities, findEnd):
    shortestDistance = math.inf
    shortestPath = ""
    trueDistance = math.inf
    
    endCity = city_node.get_node_from_name(findEnd)
    for startCity in allCityNodes:
        dist, path = ida_search_start(startCity, allCityNodes, allCities)
        if dist < shortestDistance:
            shortestDistance = dist
            trueDistance = dist
            shortestPath = path
    return shortestDistance, shortestPath, trueDistance
    
def findBestWhereStart(allCityNodes, allCities, findStart):
    shortestDistance = math.inf
    shortestPath = ""
    trueDistance = math.inf
    
    startCity = city_node.get_node_from_name(findStart)
    dist, path = ida_search_start(startCity, allCityNodes, allCities)
    if dist < shortestDistance:
        shortestDistance = dist
        trueDistance = dist
        shortestPath = path
    return shortestDistance, shortestPath, trueDistance    
    
def findTotalShortest(allCityNodes, allCities):
    shortestDistance = math.inf
    shortestPath = ""
    trueDistance = math.inf
    
    for startCity in allCityNodes:
        dist, path = ida_search_start(startCity, allCityNodes, allCities)
        if dist < shortestDistance:
            shortestDistance = dist
            trueDistance = dist
            shortestPath = path
    return shortestDistance, shortestPath, trueDistance


def heuristic(current_city, start_city):
    return city_node.get_distance(current_city, start_city)


def ida_search_start(startCity, allCityNodes, allCities):
    bound = heuristic(startCity, startCity)
    path = [startCity]
    best_cost = math.inf
    best_path_str = startCity.name

    while True:
        t, found_cost, found_path_str = search_ida(
            path=path,
            g=0.0,
            bound=bound,
            allCityNodes=allCityNodes,
            allCities=allCities,
            startCity=startCity
        )

        if t == "FOUND":
            return found_cost, found_path_str

        if t == math.inf:
            return best_cost, best_path_str

        bound = t


def search_ida(path, g, bound, allCityNodes, allCities, startCity):
    current_city = path[-1]

    if len(path) == len(allCityNodes):
        path_str = " -> ".join(city.name for city in path)
        return "FOUND", g, path_str

    f = g + heuristic(current_city, startCity)
    if f > bound:
        return f, None, None

    min_excess = math.inf

    for end_name in allCities:
        next_node = city_node.get_node_from_name(end_name)
        if next_node in path:
            continue

        cost = current_city.get_distance(end_name)
        new_g = g + cost

        path.append(next_node)
        t, found_cost, found_path_str = search_ida(
            path, new_g, bound, allCityNodes, allCities, startCity
        )
        path.pop()

        if t == "FOUND":
            return "FOUND", found_cost, found_path_str

        if isinstance(t, (int, float)) and t < min_excess:
            min_excess = t

    return min_excess, None, None


def main():
    get_nodes()


if __name__ == "__main__":
    main()
