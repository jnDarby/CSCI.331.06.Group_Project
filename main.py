"""
main.py - NY State Route Planner
Imports algorithms from separate files: ids.py, bfs.py, dfs.py, etc.
Works with FULLY CONNECTED graph (all cities have direct connections)
Integrated with Graphviz visualization and graph analysis
"""

import time
import sys

# Import algorithm classes from separate files
try:
    from Algorithms.ids import IDSAlgorithm, load_graph as ids_load_graph
    IDS_AVAILABLE = True
except ImportError:
    print("WARNING: ids.py not found")
    IDS_AVAILABLE = False

try:
    from Algorithms.bfs import BFSAlgorithm
    BFS_AVAILABLE = True
except ImportError:
    print("WARNING: bfs.py not found")
    BFS_AVAILABLE = False

try:
    from Algorithms.dfs import DFSAlgorithm
    DFS_AVAILABLE = True
except ImportError:
    print("WARNING: dfs.py not found")
    DFS_AVAILABLE = False

try:
    from Algorithms.a_star import AStarAlgorithm
    ASTAR_AVAILABLE = True
except ImportError:
    print("WARNING: Algorithms/a_star.py not found")
    ASTAR_AVAILABLE = False

try:
    from Algorithms.ida_star import IDAAlgorithm
    IDA_AVAILABLE = True
except ImportError:
    print("WARNING: Algorithms/ida_star.py not found")
    IDA_AVAILABLE = False

try:
    from Algorithms.gfs import GFSAlgorithm
    GFS_AVAILABLE = True
except ImportError:
    print("WARNING: gfs.py not found")
    GFS_AVAILABLE = False

try:
    from Algorithms.ucs import UCSAlgorithm
    UCS_AVAILABLE = True
except ImportError:
    print("WARNING: ucs.py not found")
    UCS_AVAILABLE = False

try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("WARNING: graphviz not installed (visualization disabled)")

try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("WARNING: graphviz not installed (visualization disabled)")


class NYRouteGraph:
    """Graph representation of NY cities with distance data - FULLY CONNECTED"""

    def __init__(self, csv_filename='data.csv'):
        self.filename = csv_filename
        self.cities = []
        self.graph = {}
        self.load_graph()

    def load_graph(self):
        """Load graph using the load_graph function from ids.py"""
        if IDS_AVAILABLE:
            self.graph, self.cities = ids_load_graph(self.filename)
            if self.graph:
                print(f"Graph has been loaded: {len(self.cities)} cities")
                total_edges = sum(len(neighbors) for neighbors in self.graph.values())
                print(f"Total directed edges: {total_edges}")
        else:
            print("Error: Cannot load graph without ids.py")
            sys.exit(1)

    def analyze_graph_properties(self):
        """Analyze and print basic graph properties"""
        print("\n" + "="*80)
        print("Graph Analysis")
        print("="*80)

        # Basic properties
        number_of_nodes = len(self.cities)
        number_of_edges = sum(len(neighbors) for neighbors in self.graph.values()) // 2  # undirected!

        print(f"Number of Nodes: {number_of_nodes}")
        print(f"Number of Edges: {number_of_edges}")

        # Degree stats
        degrees = []
        for city in self.cities:
            degrees.append(len(self.graph.get(city, {})))
        
        if degrees:
            print(f"\nDegree Statistics:")
            print(f"  Average Degree: {sum(degrees)/len(degrees):.2f}")
            print(f"  Min Degree: {min(degrees)}")
            print(f"  Max Degree: {max(degrees)}")

            # Find the most connected cities
            sorted_degrees = sorted([(city, len(self.graph.get(city, {}))) for city in self.cities], 
                                   key=lambda x: x[1], reverse=True)
            print(f"\nMost Connected Cities:")
            for city, deg in sorted_degrees[:5]:
                print(f"  {city}: {deg} connections")
            
            # Check connectivity
            is_connected = self.check_connectivity()
            print(f"\nGraph appears to be fully connected: {is_connected}")
        
        print("="*80 + "\n")

    def check_connectivity(self):
        """Check if the graph is connected using BFS"""
        if not self.cities:
            return False
        
        start = self.cities[0]
        visited = set()
        queue = [start]
        visited.add(start)
        
        while queue:
            current = queue.pop(0)
            for neighbor in self.graph.get(current, {}).keys():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(self.cities)

    def visualize_graphviz(self, path=None, filename='graph_visualization', format='png', show_all_edges=False):
        """Create visualization using Graphviz"""
        if not GRAPHVIZ_AVAILABLE:
            print("Graphviz Python package not available for visualization")
            return
        
        print(f"CreaIDSting graph visualization with Graphviz...")

        dot = graphviz.Graph(comment='NY State Cities', engine='neato')

        # Graph attributes for the layout
        dot.attr(overlap='false')
        dot.attr(splines='true')
        dot.attr(sep='+4.0')
        dot.attr(nodesep='4.0')
        dot.attr(ranksep='4.0')
        dot.attr(len='2.5')
        dot.attr(K='5.0')

        # Add nodes (cities)
        for city in self.cities:
            if path and city in path:
                if city == path[0]:
                    # Start node - green
                    dot.node(city, city, shape='circle', style='filled', 
                            fillcolor='lightgreen', fontsize='14', width='1.2')
                elif city == path[-1]:
                    # Goal node - red
                    dot.node(city, city, shape='doublecircle', style='filled', 
                            fillcolor='lightcoral', fontsize='14', width='1.2')
                else:
                    # Path node - yellow
                    dot.node(city, city, shape='circle', style='filled', 
                            fillcolor='yellow', fontsize='12', width='1.0')
            else:
                # Regular node - light blue
                dot.node(city, city, shape='circle', style='filled', 
                        fillcolor='lightblue', fontsize='10', width='0.8')

        # Add edges
        added_edges = set()

        if path:
            # Add path edges highlighted
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
                # Add remaining edges in gray
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
            # Show all edges
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
        
        # Render the graph
        try:
            output_path = dot.render(filename, format=format, cleanup=True)
            print(f"Graph saved to {output_path}")
        except Exception as e:
            print(f"Error rendering graph: {e}")
            print("  Make sure Graphviz is installed on your system")


def run_algorithm(actualGraph, straightlineGraph, algorithm_name, start, goal):
    """Run selected algorithm using imported classes"""
    
    algo = None
    
    if algorithm_name == "IDS" and IDS_AVAILABLE:
        algo = IDSAlgorithm(actualGraph.graph)
    elif algorithm_name == "BFS" and BFS_AVAILABLE:
        algo = BFSAlgorithm(actualGraph.graph)
    elif algorithm_name == "DFS" and DFS_AVAILABLE:
        algo = DFSAlgorithm(actualGraph.graph)
    elif algorithm_name == "UCS" and UCS_AVAILABLE:
        algo = UCSAlgorithm(actualGraph.graph)
    elif algorithm_name == "GFS" and GFS_AVAILABLE:
        algo = GFSAlgorithm(actualGraph.graph)
    elif algorithm_name == "IDA_STAR" and IDA_AVAILABLE:
        algo = IDAAlgorithm(actualGraph.graph, straightlineGraph.graph)
    elif algorithm_name == "A_STAR" and ASTAR_AVAILABLE:
        algo = AStarAlgorithm(actualGraph.graph, straightlineGraph.graph)
    else:
        print(f"Algorithm {algorithm_name} not available")
        return None
    
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
    """Main application - imports algorithms from separate files"""
    
    print("="*80)
    print("NY STATE ROUTE PLANNER - Graphviz Integration")
    print("="*80 + "\n")
    
    # Load graph
    actualGraph = NYRouteGraph('actualDistance.csv')
    straightLineGraph = NYRouteGraph('straightLineDistance.csv')
    
    if not actualGraph.graph:
        print("Failed to load graph. Exiting.")
        sys.exit(1)

    if not straightLineGraph.graph:
        print("Failed to load graph. Exiting.")
        sys.exit(1)
    
    # Analyze graph properties
    actualGraph.analyze_graph_properties()
    straightLineGraph.analyze_graph_properties()
    
    # Create full network visualization
    if GRAPHVIZ_AVAILABLE:
        print("Creating full network visualization...")
        actualGraph.visualize_graphviz(filename='full_network', format='png')
        straightLineGraph.visualize_graphviz(filename='full_network', format='png')
        print()
    
    # Show available algorithms
    print("\n" + "="*80)
    print("Available Algorithms:")
    algo_list = []
    if IDS_AVAILABLE:
        algo_list.append("IDS")
        print("  - IDS  (Iterative Deepening Search)")
    if BFS_AVAILABLE:
        algo_list.append("BFS")
        print("  - BFS  (Breadth-First Search)")
    if DFS_AVAILABLE:
        algo_list.append("DFS")
        print("  - DFS  (Depth-First Search)")
    if UCS_AVAILABLE:
        algo_list.append("UCS")
        print("  - UCS  (Uniform-Cost Search)")
    if GFS_AVAILABLE:
        algo_list.append("GFS")
        print("  - GFS  (Greedy First Search)")
    if IDA_AVAILABLE:
        algo_list.append("IDA_STAR")
        print("  - IDA_STAR")
    if ASTAR_AVAILABLE:
        algo_list.append("A_STAR")
        print("  - A_STAR")
    
    if not algo_list:
        print("ERROR: No algorithm files found!")
        sys.exit(1)
    
    print("="*80 + "\n")
    
    # Get algorithm choice
    while True:
        choice = input(f"Select algorithm ({'/'.join(algo_list)}): ").strip().upper()
        if choice in algo_list:
            algorithm = choice
            break
        print(f"Invalid choice. Please select from: {', '.join(algo_list)}")
    
    # Start city is always Rochester
    start = 'Rochester'
    
    # Check if Rochester exists in the graph
    if start not in actualGraph.cities:
        print(f"\nERROR: '{start}' not found in the graph!")
        print(f"Available cities: {', '.join(sorted(actualGraph.cities))}")
        print("\nPlease check your data.csv file. Make sure 'Rochester' is spelled correctly.")
        sys.exit(1)
    
    # Get destination city
    print(f"\nStarting city: {start}")
    print(f"Available destinations: {', '.join(sorted(actualGraph.cities[:10]))}... (and {len(actualGraph.cities)-10} more)")
    
    while True:
        goal = input("\nEnter destination city (default: New York City): ").strip()
        if not goal:
            goal = 'New York City'
        if goal in actualGraph.cities:
            break
        print(f"'{goal}' not found. Please try again.")
    
    print(f"\nRunning {algorithm}: {start} → {goal}\n")
    
    # Run search
    result = run_algorithm(actualGraph, straightLineGraph, algorithm, start, goal)
    
    # Print results
    print_results(result)
    
    # Visualize the path
    if GRAPHVIZ_AVAILABLE and result and result['path']:
        print("Creating path visualization...")
        actualGraph.visualize_graphviz(
            result['path'], 
            filename=f'{algorithm.lower()}_route_{start.replace(" ", "_")}_to_{goal.replace(" ", "_")}',
            format='png',
            show_all_edges=False  # Only show path edges
        )
        
        print("\nCreating path visualization with all edges...")
        actualGraph.visualize_graphviz(
            result['path'], 
            filename=f'{algorithm.lower()}_route_{start.replace(" ", "_")}_to_{goal.replace(" ", "_")}_full',
            format='png',
            show_all_edges=True  # Show all edges and highlight the path
        )
        print()
    
    # Ask if user wants to run all destinations
    run_all = input("\nRun algorithm for all destinations from start city? (y/n): ").strip().lower()
    
    if run_all == 'y':
        print("\n" + "="*80)
        print(f"ALL ROUTES FROM {start} ({algorithm})")
        print("="*80)
        print(f"{'Destination':<20} {'Distance':<12} {'Stops':<8} {'Expanded':<10} {'Time (ms)'}")
        print("-"*80)
        
        results = []
        for city in sorted(actualGraph.cities):
            if city == start:
                continue
            
            result = run_algorithm(actualGraph, straightLineGraph, algorithm, start, city)
            if result and result['path']:
                print(f"{city:<20} {result['cost']:<12.2f} {result['stops']:<8} "
                      f"{result['expanded']:<10} {result['runtime']:<.4f}")
                results.append(result)
            else:
                print(f"{city:<20} {'NO PATH FOUND':<12} {'-':<8} {'-':<10} {'-'}")
        
        print("="*80)
        
        # Summary statistics
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
        print(f"  - {algorithm.lower()}_route_{start.replace(' ', '_')}_to_{goal.replace(' ', '_')}.png (path only)")
        print(f"  - {algorithm.lower()}_route_{start.replace(' ', '_')}_to_{goal.replace(' ', '_')}_full.png (path with context)")


if __name__ == "__main__":
    main()