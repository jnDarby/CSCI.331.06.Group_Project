
import heapq

class GFSAlgorithm:
    """
    Greedy Best-First Search (GBFS)
    GFS/GBFS uses the heuristic/straight line distance to guide the search towards a specific goal,
    but it tracks actual road distance for the path cost.
    """
    
    def __init__(self, actual_graph, heuristic_graph):
        """
        mow initalize wiht both of the graphs
        """
        self.actual_graph = actual_graph
        self.heuristic_graph = heuristic_graph
        self.expanded_nodes = 0
    
    def search(self, start, goal):
        """
        this works to return the paht tuple where the path is the list of
        cities from start to goal and the cost is the actual road distance 
        traveled
        """
        if start == goal:
            return ([start], 0)
        
        if start not in self.actual_graph or start not in self.heuristic_graph:
            return (None, 0)
        
        self.expanded_nodes = 0
        
        # getting the heuristic value for a city (straight-line distance to goal)
        def h(city):
            return self.heuristic_graph.get(city, {}).get(goal, float('inf'))
        
        # priority queue now: (heuristic_value, current_city, path_so_far, actual_cost_so_far)
        frontier = [(h(start), start, [start], 0)]
        visited = set()
        
        while frontier:
            _, current, path, actual_cost = heapq.heappop(frontier)
            
            # skip if already visited
            if current in visited:
                continue
            
            visited.add(current)
            self.expanded_nodes += 1
            
            # goal check
            if current == goal:
                return (path, actual_cost)
            
            # expand neighbors, prioritized by heuristic value (straight-line distance to goal)
            for neighbor in self.actual_graph.get(current, {}):
                if neighbor not in visited:
                    # get the ACTUAL road distance HERE for cost calculation
                    actual_edge_cost = self.actual_graph[current][neighbor]
                    new_path = path + [neighbor]
                    new_actual_cost = actual_cost + actual_edge_cost
                    
                    # priority is ONLY the heuristic (straight-line distance to goal)
                    h_value = h(neighbor)
                    heapq.heappush(frontier, (h_value, neighbor, new_path, new_actual_cost))
        
        # no path found
        return (None, 0)