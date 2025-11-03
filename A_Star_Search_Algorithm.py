import math
import csv

filename = 'data.csv'

allCities = []
routes = {}

def loadValues():
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

        for startCity in allCities:
            for endCity in allCities:
                print(startCity + " and " + endCity + " distance is " + str(routes[(startCity,endCity)]))

def findShortestAPath():
    for startCity in allCities:
        for endCity in allCities:
            if startCity == endCity:
                break
            else:
                aSearch(startCity, endCity, allCities)

def aSearch(start: str, end: str, cities):
    totalDistance = 0
    path = ""
    currentCity = start
    
    for next in allCities:
        estPathValue(currentCity, next)
        
def estPathValue():
    return None
    

def main():
    loadValues()
    findShortestAPath()

if __name__ == "__main__":
    main()