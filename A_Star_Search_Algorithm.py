import math
import csv

filename = 'data.csv'

allCities = []
routes = {}

with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Read the header row with city names
    allCities = header[0:]  # Store values
    for row in reader:
        city_from = row[0]  # first cell in the row is the city name            
        distances = row[1:]
            
    for city_to, distance_str in zip(allCities, distances):
        distance = float(distance_str)
        # Use tuple keys for clarity and avoid shortening
        routes[(city_from,city_to)] = distance

        for route in routes:
            print(str(route) + " is " + str(routes[route]))

def findShortestAPath():
    shortestDistance = math.inf
    current = 0
    shortestPath = ""
    for startCity in allCities:
            current = aSearch(startCity, allCities)
            if(current[0] < shortestDistance):
                shortestDistance = current[0]
                shortestPath = current[1]
    print("The shortest path is " + shortestPath + " with a direct line distance of " + str(shortestDistance) + " miles.")

def aSearch(start: str, cities):
    
    totalDistance = 0
    path = str(start) + " -> All Cities"
     
    return (totalDistance,path)
    

def main():
    findShortestAPath()

if __name__ == "__main__":
    main()