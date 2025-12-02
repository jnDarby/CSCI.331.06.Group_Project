"""
main.py - NY State Route Planner
Imports algorithms from separate files: ids.py, bfs.py, dfs.py
User selects which algorithm to run
Integrated with Graphviz visualization
"""

import time
import sys

# Import algorithm classes from separate files
try:
    from ids import IDSAlgorithm, load_graph as ids_load_graph
    IDS_AVAILABLE = True
except ImportError:
    print("WARNING: ids.py not found")
    IDS_AVAILABLE = False

try:
    from bfs import BFSAlgorithm
    BFS_AVAILABLE = True
except ImportError:
    print("WARNING: bfs.py not found")
    BFS_AVAILABLE = False

try:
    from dfs import DFSAlgorithm
    DFS_AVAILABLE = True
except ImportError:
    print("WARNING: dfs.py not found")
    DFS_AVAILABLE = False

try:
    from a_start_search import AStarAlgorithm
    DFS_AVAILABLE = True
except ImportError:
    print("WARNING: a_start_search.py not found")
    DFS_AVAILABLE = False

try:
    from ida import IDAAlgorithm
    DFS_AVAILABLE = True
except ImportError:
    print("WARNING: ida.py not found")
    DFS_AVAILABLE = False

try:
    from gfs import GFSAlgorithm
    DFS_AVAILABLE = True
except ImportError:
    print("WARNING: gfs.py not found")
    DFS_AVAILABLE = False

try:
    from ucs import UCSAlgorithm
    DFS_AVAILABLE = True
except ImportError:
    print("WARNING: ucs.py not found")
    DFS_AVAILABLE = False

try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("WARNING: graphviz not installed (visualization disabled)")


class NYRouteGraph:
    """Graph representation with visualization capabilities"""
    
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
                print(f"Graph loaded: {len(self.cities)} cities")
                total_edges = sum(len(neighbors) for neighbors in self.graph.values())
                print(f"Total directed edges: {total_edges}")
        else:
            print("Error: Cannot load graph without ids.py")
            sys.exit(1)
    
    def visualize_graphviz(self, path=None, filename='graph_visualization', format='png', show_all_edges=False):
        """Create visualization using Graphviz"""
        if not GRAPHVIZ_AVAILABLE:
            print("Graphviz not available for visualization")
            return
        
        print(f"Creating graph visualization...")
        
        dot = graphviz.Graph(comment='NY State Cities', engine='neato')
        dot.attr(overlap='false', splines='true', sep='+0.5', nodesep='1.5')
        
        # add the nodes as the cities
        for city in self.cities:
            if path and city in path:
                if city == path[0]:
                    dot.node(city, city, shape='circle', style='filled', 
                            fillcolor='lightgreen', fontsize='14', width='1.2')
                elif city == path[-1]:
                    dot.node(city, city, shape='doublecircle', style='filled', 
                            fillcolor='lightcoral', fontsize='14', width='1.2')
                else:
                    dot.node(city, city, shape='circle', style='filled', 
                            fillcolor='yellow', fontsize='12', width='1.0')
            else:
                dot.node(city, city, shape='circle', style='filled', 
                        fillcolor='lightblue', fontsize='10', width='0.8')
        
        # Add edges
        added_edges = set()
        
        if path:
            # and highlight path edges/make the path highlighted in a different color
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
                # now we gotta add remaining edges in gray
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
            # show all edges finally
            for city_from in self.graph:
                for city_to in self.graph[city_from]:
                    edge = tuple(sorted([city_from, city_to]))
                    if edge not in added_edges:
                        distance = self.graph[city_from][city_to]
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
        
        try:
            output_path = dot.render(filename, format=format, cleanup=True)
            print(f"Graph saved to {output_path}")
        except Exception as e:
            print(f"Error rendering graph: {e}")


def run_algorithm(graph, algorithm_name, start, goal):
    """Run selected algorithm using imported classes"""
    
    algo = None
    
    if algorithm_name == "IDS" and IDS_AVAILABLE:
        algo = IDSAlgorithm(graph.graph)
    elif algorithm_name == "BFS" and BFS_AVAILABLE:
        algo = BFSAlgorithm(graph.graph)
    elif algorithm_name == "DFS" and DFS_AVAILABLE:
        algo = DFSAlgorithm(graph.graph)
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
    """Main application"""
    
    print("="*80)
    print("NY STATE ROUTE PLANNER")
    print("="*80 + "\n")
    
    # now we gotta load graph
    graph = NYRouteGraph('data.csv')
    
    if not graph.graph:
        print("Failed to load graph. Exiting.")
        sys.exit(1)
    
    # show available algorithms
    print("\nAvailable Algorithms:")
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
    
    if not algo_list:
        print("ERROR: No algorithm files found!")
        print("Make sure ids.py, bfs.py, and/or dfs.py are in the same directory")
        sys.exit(1)
    
    print()
    
    # get the algorithm choice first
    while True:
        choice = input(f"Select algorithm ({'/'.join(algo_list)}): ").strip().upper()
        if choice in algo_list:
            algorithm = choice
            break
        print(f"Invalid choice. Please select from: {', '.join(algo_list)}")
    
    # then get the start and goal cities which can be changed but will default to NYC and ROC
    print(f"\nAvailable cities: {', '.join(sorted(graph.cities[:10]))}... (and {len(graph.cities)-10} more)")
    
    while True:
        start = input("\nEnter start city (default: Rochester): ").strip()
        if not start:
            start = 'Rochester'
        if start in graph.cities:
            break
        print(f"'{start}' not found. Please try again.")
    
    while True:
        goal = input("Enter destination city (default: New York City): ").strip()
        if not goal:
            goal = 'New York City'
        if goal in graph.cities:
            break
        print(f"'{goal}' not found. Please try again.")
    
    print(f"\nRunning {algorithm}: {start} → {goal}\n")
    
    # run the algorithm chosen
    result = run_algorithm(graph, algorithm, start, goal)
    
    # print results out
    print_results(result)
    
    # visualize the path using graphviz
    if GRAPHVIZ_AVAILABLE and result and result['path']:
        print("Creating visualizations...")
        graph.visualize_graphviz(
            result['path'],
            filename=f'{algorithm.lower()}_route_{start.replace(" ", "_")}_to_{goal.replace(" ", "_")}',
            format='png',
            show_all_edges=True
        )
        print()
    
    # now we gotta ask the user if the user wants to run all destinations
    run_all = input("\nRun algorithm for all destinations from start city? (y/n): ").strip().lower()
    
    if run_all == 'y':
        print("\n" + "="*80)
        print(f"ALL ROUTES FROM {start} ({algorithm})")
        print("="*80)
        print(f"{'Destination':<20} {'Distance':<12} {'Stops':<8} {'Expanded':<10} {'Time (ms)'}")
        print("-"*80)
        
        results = []
        for city in sorted(graph.cities):
            if city == start:
                continue
            
            result = run_algorithm(graph, algorithm, start, city)
            if result and result['path']:
                print(f"{city:<20} {result['cost']:<12.2f} {result['stops']:<8} "
                      f"{result['expanded']:<10} {result['runtime']:<.4f}")
                results.append(result)
            else:
                print(f"{city:<20} {'NO PATH':<12} {'-':<8} {'-':<10} {'-'}")
        
        print("="*80)
        
        # overall summary of the results 
        if results:
            avg_dist = sum(r['cost'] for r in results) / len(results)
            avg_stops = sum(r['stops'] for r in results) / len(results)
            avg_expanded = sum(r['expanded'] for r in results) / len(results)
            
            print(f"\nAverage Distance: {avg_dist:.2f} miles")
            print(f"Average Stops: {avg_stops:.2f}")
            print(f"Average Nodes Expanded: {avg_expanded:.2f}")
    
    print("\n✓ Complete!")


if __name__ == "__main__":
    main()