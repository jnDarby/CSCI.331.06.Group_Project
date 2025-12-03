"""
ids.py - Iterative Deepening Search Algorithm
Works with fully connected graph (all cities have direct connections)
IDS finds paths with fewest hops, not shortest distance
"""

import csv
import time

class IDSAlgorithm:
    """IDS Implementation"""
    
    def __init__(self, graph):
        self.graph = graph
        self.expanded_nodes = 0
    
    def dls(self, current, goal, depth_limit, path, cost):
        """Depth-limited search helper function"""
        self.expanded_nodes += 1
        
        if current == goal:
            return (path + [current], cost)
        
        if depth_limit == 0:
            return (None, 0)
        
        neighbors = sorted(self.graph.get(current, {}).keys())
        
        for neighbor in neighbors:
            if neighbor not in path:  # Avoid cycles
                edge_cost = self.graph[current][neighbor]
                result, total_cost = self.dls(
                    neighbor, goal, depth_limit - 1,
                    path + [current], cost + edge_cost
                )
                if result:
                    return (result, total_cost)
        
        return (None, 0)
    
    def search(self, start, goal, max_depth=50):
        """Run IDS algorithm - finds path with fewest stops"""
        self.expanded_nodes = 0
        
        for depth in range(max_depth):
            result, total_cost = self.dls(start, goal, depth, [], 0)
            if result:
                return (result, total_cost)
        
        return (None, 0)


def load_graph(filename='data.csv'):
    """
    Load graph from CSV file - FULLY CONNECTED format
    Expects format: first row/column are city names, rest are distances
    """
    cities = []
    graph = {}
    
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            lines = list(reader)
            
            if not lines:
                raise ValueError("CSV file is empty")
            
            # First row is header with city names
            header = lines[0]
            # Get ALL city names from header (don't skip first column)
            cities = [city.strip() for city in header if city.strip()]
            
            # Build adjacency dictionary from remaining rows
            for row in lines[1:]:
                if not row or len(row) == 0:
                    continue
                
                city_from = row[0].strip()
                if not city_from:
                    continue
                
                distances = row[1:]  # Skip first column (city name)
                graph[city_from] = {}
                
                # Map distances to cities
                # The distances align with ALL cities in the header (including the first one)
                for i, distance_str in enumerate(distances):
                    if i >= len(cities):
                        break
                    
                    city_to = cities[i]
                    
                    # Skip self-loops (city to itself)
                    if city_from == city_to:
                        continue
                    
                    try:
                        distance = float(distance_str.strip())
                        # Add edge for any positive distance
                        if distance > 0:
                            graph[city_from][city_to] = distance
                    except (ValueError, AttributeError):
                        # Skip empty or invalid values
                        continue
        
        print(f"Graph loaded: {len(cities)} cities")
        total_connections = sum(len(neighbors) for neighbors in graph.values())
        print(f"Total connections: {total_connections}")
        
        return graph, cities
        
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'")
        return None, None
    except Exception as e:
        print(f"Error loading CSV: {e}")
        import traceback
        traceback.print_exc()
        return None, None


# If run as standalone script
if __name__ == "__main__":
    print("="*80)
    print("IDS Algorithm - Standalone Mode")
    print("="*80)
    print("NOTE: IDS finds paths with FEWEST HOPS, not shortest distance")
    print("="*80 + "\n")
    
    graph, cities = load_graph('data.csv')
    
    if not graph:
        print("Failed to load graph")
        exit(1)
    
    start = 'Rochester'
    
    print(f"\nRunning IDS from {start} to all destinations\n")
    print(f"{'Destination':<20} {'Distance':<12} {'Stops':<8} {'Expanded':<10} {'Time (ms)'}")
    print("-"*80)
    
    all_results = []
    
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
            all_results.append({
                'destination': goal,
                'path': path,
                'cost': cost,
                'stops': stops,
                'expanded': algo.expanded_nodes
            })
        else:
            print(f"{goal:<20} {'NO PATH':<12} {'-':<8} {'-':<10} {'-'}")
    
    print("="*80)
    
    # Show example of IDS behavior
    if all_results:
        print("\n" + "="*80)
        print("EXAMPLE: Rochester → New York City")
        print("="*80)
        
        nyc_result = next((r for r in all_results if r['destination'] == 'New York City'), None)
        if nyc_result:
            print(f"Path found: {' → '.join(nyc_result['path'])}")
            print(f"Total Distance: {nyc_result['cost']:.2f} miles")
            print(f"Number of Stops: {nyc_result['stops']}")
            print(f"Nodes Expanded: {nyc_result['expanded']}")
            print("\nNOTE: With a fully connected graph, IDS will likely find")
            print("      the DIRECT path (1 stop) since it minimizes hops.")
            print("      For shortest DISTANCE, use UCS or A* instead.")
        
        print("="*80)