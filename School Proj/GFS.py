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

    for startCity in allCities:
        for endCity in allCities:
            print(startCity + " and " + endCity + " distance is " + str(routes[(startCity,endCity)]))

def greedyFirst():
    totalDistance = 0
    path = ""
    cost = math.inf
    for start in allCities:
        for end in allCities:
            if( start != end and routes[(start,end)] < cost):
                cost = routes[(start,end)]
                route = (start,end)
                path = start + " -> " + end
    totalDistance += cost
    del routes[route]
    allCities.remove(route[0])
    lastCity = route[1]
    while(True):
        cost = math.inf

        for end in allCities:
            if( lastCity != end and routes[(lastCity,end)] < cost):
                cost = routes[(lastCity,end)]
                route = (lastCity,end)
        for city in route:
            if(city not in path):
                path += " -> " + city
                allCities.remove(city)
        totalDistance += cost
        del routes[route]
        
        if(len(allCities) < 2):
            print(path)
            print("Total Distance: " + str(totalDistance) + " Miles")
            break



greedyFirst()
print("End")