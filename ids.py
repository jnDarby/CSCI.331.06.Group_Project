"""
ids.py - Iterative Deepening Search Algorithm
"""

import csv
import time

class IDSAlgorithm:
    """IDS Implementation"""
    
    def __init__(self, graph):
        self.graph = graph
        self.expanded_nodes = 0
    
    def dls(self, current, goal, depth_limit, path, cost):
        """depth-limited search helper function"""
        self.expanded_nodes += 1
        
        if current == goal:
            return (path + [current], cost)
        
        if depth_limit == 0:
            return (None, 0)
        
        neighbors = sorted(self.graph.get(current, {}).keys())
        
        for neighbor in neighbors:
            if neighbor not in path:
                edge_cost = self.graph[current][neighbor]
                result, total_cost = self.dls(
                    neighbor, goal, depth_limit - 1,
                    path + [current], cost + edge_cost
                )
                if result:
                    return (result, total_cost)
        
        return (None, 0)
    
    def search(self, start, goal, max_depth=50):
        """running the IDS algorithm"""
        self.expanded_nodes = 0
        
        for depth in range(max_depth):
            result, total_cost = self.dls(start, goal, depth, [], 0)
            if result:
                return (result, total_cost)
        
        return (None, 0)


def load_graph(filename='data.csv'):
    """load in the graph from CSV file - this should handle the new csv file"""
    cities = []
    graph = {}
    
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            lines = list(reader)
            
            if not lines:
                raise ValueError("CSV file is empty")
            
            # header with city names (skip first empty column)
            cities = [city.strip() for city in lines[0][1:] if city.strip()]
            
            # build adjacency dictionary
            for row in lines[1:]:
                if not row or len(row) == 0:
                    continue
                
                city_from = row[0].strip()
                if not city_from:
                    continue
                
                distances = row[1:]
                graph[city_from] = {}
                
                for i, distance_str in enumerate(distances):
                    if i >= len(cities):
                        break
                    
                    city_to = cities[i]
                    
                    # skip empty cells (no direct connection)
                    if not distance_str or distance_str.strip() == '':
                        continue
                    
                    try:
                        distance = float(distance_str.strip())
                        if distance > 0:
                            graph[city_from][city_to] = distance
                    except ValueError:
                        continue
        
        return graph, cities
        
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'")
        return None, None
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None, None


# IF its alone then run as standalone script
if __name__ == "__main__":
    print("="*80)
    print("IDS Algorithm - Standalone Mode")
    print("="*80)
    
    graph, cities = load_graph('data.csv')
    
    if not graph:
        print("Failed to load graph")
        exit(1)
    
    print(f"Graph loaded: {len(cities)} cities\n")
    
    start = 'Rochester'
    
    print(f"Running IDS from {start} to all destinations\n")
    print(f"{'Destination':<20} {'Distance':<12} {'Stops':<8} {'Expanded':<10} {'Time (ms)'}")
    print("-"*80)
    
    for goal in sorted(cities):
        if goal == start:
            continue
        
        algo = IDSAlgorithm(graph)
        start_time = time.time()
        path, cost = algo.search(start, goal)
        end_time = time.time()
        runtime = (end_time - start_time) * 1000
        
        if path:
            stops = len(path) - 1
            print(f"{goal:<20} {cost:<12.2f} {stops:<8} {algo.expanded_nodes:<10} {runtime:<.4f}")
        else:
            print(f"{goal:<20} {'NO PATH':<12} {'-':<8} {'-':<10} {'-'}")
    
    print("="*80)