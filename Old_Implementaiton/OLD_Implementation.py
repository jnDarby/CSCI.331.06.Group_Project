"""
NY State Route Planner for the Main Application
Integrated with search algos with Graphviz visualizaiton
"""

import csv
import time
import sys
import os

try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("WARNING: graphviz Python package not installed.")
    print("Install with: python -m pip install graphviz")
    print()

class NYRouteGraph:
    """Graph Representation of NY Cities with distance data included"""

    def __init__(self, csv_filename='data.csv'):
        self.filename = csv_filename
        self.cities = []
        self.graph = {}
        self.load_graph()

    def load_graph(self):
        """Load the graph from the CSV file"""
        try:
            with open(self.filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                lines = list(reader)
                if not lines:
                    raise ValueError("CSV file is empty, please retry")
                
            # header with the city names
            self.cities = lines[0]

            # now its building the adjacency dictionairy
            for row in lines[1:]:
                if not row or len(row) == 0:
                    continue

                city_from = row[0]
                distances = row[1:]

                self.graph[city_from] = {}

                for city_to, distance_str in zip(self.cities, distances):
                    try:
                        distance = float(distance_str)
                        if distance > 0:
                            self.graph[city_from][city_to] = distance
                    except ValueError:
                        continue
            print(f"Graph has been loaded: {len(self.cities)} cities")
        except FileNotFoundError:
            print(f"Error: Couldn't find the file '{self.filename}'")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            sys.exit(1)

    def analyze_graph_properties(self):
        """Analyze and print basic graph properties"""
        print("\n" + "="*80)
        print("Graph Analysis")
        print("="*80)

        # basic properties
        number_of_nodes = len(self.cities)
        number_of_edges = sum(len(neighbors) for neighbors in self.graph.values()) // 2 # undirected!

        print(f"Number of Nodes: {number_of_nodes}")
        print(f"Number of Edges: {number_of_edges}")

        # degree stats
        degrees = []
        for city in self.cities:
            degrees.append(len(self.graph.get(city, {})))
        
        print(f"\nDegree Statistics:")
        print(f"  Average Degree: {sum(degrees)/len(degrees):.2f}")
        print(f"  Min Degree: {min(degrees)}")
        print(f"  Average Degree: {max(degrees)}")

        # find the most connected cities
        sorted_degrees = sorted([(city, len(self.graph.get(city, {}))) for city in self.cities], 
                               key=lambda x: x[1], reverse=True)
        print(f"\nMost Connected Cities:")
        for city, deg in sorted_degrees[:5]:
            print(f"  {city}: {deg} connections")
        
        print(f"\nGraph appears to be fully connected: {all(len(self.graph.get(city, {})) > 0 for city in self.cities)}")

        print("="*80 + "\n")

    def visualize_graphviz(self, path=None, filename='graph_visulization', format='png', show_all_edges=False):
        """
        Create the visualization using Graphviz taking in args of the path/the list of cities to highlight, filename which is the output for the filename, the format is teh output format, and show all edges is if its false and path is provided only show the path edges"""

        if not GRAPHVIZ_AVAILABLE:
            print("Graphviz Python package not available for visualization")
            return
        
        print(f"Creating graph visualization with Graphviz...")

        dot = graphviz.Graph(comment='NY State Cities', engine='neato')

        # graph attributes for the layout
        dot.attr(overlap='false')
        dot.attr(splines='true')
        dot.attr(sep='+0.5')
        dot.attr(nodesep='1.5')

        # add in the nodes aka the cities
        for city in self.cities:
            if path and city in path:
                if city == path[0]:
                    # start node - green
                    dot.node(city, city, shape='circle', style='filled', 
                            fillcolor='lightgreen', fontsize='14', width='1.2')
                elif city == path[-1]:
                    # Goal node - red
                    dot.node(city, city, shape='doublecircle', style='filled', 
                            fillcolor='lightcoral', fontsize='14', width='1.2')
                else:
                    # path node - yellow
                    dot.node(city, city, shape='circle', style='filled', 
                            fillcolor='yellow', fontsize='12', width='1.0')
            else:
                # regular node - light blue
                dot.node(city, city, shape='circle', style='filled', 
                        fillcolor='lightblue', fontsize='10', width='0.8')

        # add in the edges
        added_edges = set()

        if path:
            # add path edges highlighted
            for i in range(len(path) - 1):
                city_from = path[i]
                city_to = path[i+1]

                if city_to in self.graph.get(city_from, {}):
                    distance = self.graph[city_from][city_to]
                    edge = tuple(sorted([city_from, city_to]))

                    if edge not in added_edges:
                        dot.edge(city_from, city_to,
                                 label=f'{distance:.1f}',
                                 color='red',
                                 penwidth='3.0',
                                 fontsize='12',
                                 fontcolor='red')
                        added_edges.add(edge)

            if show_all_edges:
                # add in the remaining edges
                for city_from in self.graph:
                    for city_to in self.graph[city_from]:
                        edge = tuple(sorted([city_from, city_to]))
                        if edge not in added_edges:
                            distance = self.graph[city_from][city_to]
                            dot.edge(city_from, city_to,
                                     label=f'{distance:.1f}', 
                                    color='gray', 
                                    penwidth='0.5',
                                    fontsize='8',
                                    fontcolor='gray')
                            added_edges.add(edge)
        else:
            # show all edges
            for city_from in self.graph:
                for city_to in self.graph[city_from]:
                    edge = tuple(sorted([city_from, city_to]))
                    if edge not in added_edges:
                        distance = self.graph[city_from][city_to]
                        # Show edge labels only for shorter distances to reduce clutter
                        if distance < 100:
                            dot.edge(city_from, city_to, 
                                    label=f'{distance:.0f}', 
                                    color='gray70', 
                                    penwidth='1.0',
                                    fontsize='8')
                        else:
                            dot.edge(city_from, city_to, 
                                    color='gray80', 
                                    penwidth='0.5')
                        added_edges.add(edge)
        
        # render the graph
        try:
            output_path = dot.render(filename, format=format, cleanup=True)
            print(f"Graph saved to {output_path}")
        except Exception as e:
            print(f"Error rendering graph: {e}")
            print("  Make sure Graphviz is installed on your system:")

class SearchAlgorithms:
    """Base class for search algorithms"""
    
    def __init__(self, graph):
        self.graph = graph
        self.expanded_nodes = 0
        
    def search(self, start, goal):
        """Override in subclass"""
        raise NotImplementedError

class IDSAlgorithm(SearchAlgorithms):
    """Iterative Deepening Search"""
    
    def dls(self, current, goal, depth_limit, path, cost):
        """Depth-Limited Search helper"""
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
        """Run IDS"""
        self.expanded_nodes = 0
        
        for depth in range(max_depth):
            result, total_cost = self.dls(start, goal, depth, [], 0)
            if result:
                return (result, total_cost)
        
        return (None, 0)


def run_algorithm(graph, algorithm_name, start, goal):
    """Run a search algorithm and return results"""
    
    if algorithm_name == "IDS":
        algo = IDSAlgorithm(graph.graph)
        
        start_time = time.time()
        path, cost = algo.search(start, goal)
        end_time = time.time()
        
        return {
            'algorithm': algorithm_name,
            'path': path,
            'cost': cost,
            'expanded': algo.expanded_nodes,
            'runtime': (end_time - start_time) * 1000,
            'stops': len(path) - 1 if path else 0
        }
    
    return None


def print_results(result):
    """Print formatted results"""
    if not result or not result['path']:
        print("No path found!")
        return
    
    print("\n" + "="*80)
    print(f"RESULTS: {result['algorithm']} Algorithm")
    print("="*80)
    print(f"Path: {' → '.join(result['path'])}")
    print(f"Total Distance: {result['cost']:.2f} miles")
    print(f"Number of Stops: {result['stops']}")
    print(f"Nodes Expanded: {result['expanded']}")
    print(f"Runtime: {result['runtime']:.4f} ms")
    print("="*80 + "\n")


def main():
    """Main application"""
    
    print("="*80)
    print("NY STATE ROUTE PLANNER - Graphviz Integration")
    print("="*80 + "\n")
    
    # Load graph
    graph = NYRouteGraph('data.csv')
    
    # Analyze graph
    graph.analyze_graph_properties()
    
    # Create full network visualization
    if GRAPHVIZ_AVAILABLE:
        print("Creating full network visualization...")
        graph.visualize_graphviz(filename='full_network', format='png')
        print()
    
    # Default search
    start = 'Rochester'
    goal = 'New York City'
    
    print(f"Running IDS: {start} → {goal}\n")
    
    # Run search
    result = run_algorithm(graph, "IDS", start, goal)
    
    # Print results
    print_results(result)
    
    # Visualize the path
    if GRAPHVIZ_AVAILABLE and result and result['path']:
        print("Creating path visualization...")
        graph.visualize_graphviz(
            result['path'], 
            filename='ids_route_rochester_to_nyc',
            format='png',
            show_all_edges=False  # Only show path edges
        )
        
        print("\nCreating path visualization with all edges...")
        graph.visualize_graphviz(
            result['path'], 
            filename='ids_route_rochester_to_nyc_full',
            format='png',
            show_all_edges=True  # Show all edges, path highlighted
        )
        print()
    
    # All destinations from Rochester
    print("\n" + "="*80)
    print(f"ALL ROUTES FROM {start} (IDS)")
    print("="*80)
    print(f"{'Destination':<20} {'Distance':<12} {'Stops':<8} {'Expanded':<10} {'Time (ms)'}")
    print("-"*80)
    
    results = []
    for city in sorted(graph.cities):
        if city == start:
            continue
        
        result = run_algorithm(graph, "IDS", start, city)
        if result and result['path']:
            print(f"{city:<20} {result['cost']:<12.2f} {result['stops']:<8} "
                  f"{result['expanded']:<10} {result['runtime']:<.4f}")
            results.append(result)
    
    print("="*80)
    
    # Summary
    if results:
        avg_dist = sum(r['cost'] for r in results) / len(results)
        avg_stops = sum(r['stops'] for r in results) / len(results)
        avg_expanded = sum(r['expanded'] for r in results) / len(results)
        
        print(f"\nAverage Distance: {avg_dist:.2f} miles")
        print(f"Average Stops: {avg_stops:.2f}")
        print(f"Average Nodes Expanded: {avg_expanded:.2f}")
    
    print("\n✓ Complete!")
    
    if GRAPHVIZ_AVAILABLE:
        print("\nGenerated files:")
        print("  - full_network.png (complete network)")
        print("  - ids_route_rochester_to_nyc.png (path only)")
        print("  - ids_route_rochester_to_nyc_full.png (path with context)")


if __name__ == "__main__":
    main()