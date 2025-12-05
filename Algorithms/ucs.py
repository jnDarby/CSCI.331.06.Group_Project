import heapq

class UCSAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.expanded_nodes = 0
    
    def search(self, start, goal):
        """
        Search for a path from start to goal using Uniform Cost Search.
        Returns: (path, cost) tuple
        """
        if start == goal:
            return ([start], 0)
            
        self.expanded_nodes = 0
        
        # Priority queue: (cost, current_city)
        frontier = [(0, start)]
        cost_so_far = {start: 0}
        came_from = {}
        expanded = set()  # Track which nodes we've already expanded
        
        while frontier:
            current_cost, current = heapq.heappop(frontier)
            
            # Skip if already expanded
            if current in expanded:
                continue
            
            # Mark as expanded
            expanded.add(current)
            self.expanded_nodes += 1
            
            # Goal test when popping
            if current == goal:
                # Reconstruct path
                path = []
                node = goal
                while node in came_from:
                    path.append(node)
                    node = came_from[node]
                path.append(start)
                return (path[::-1], current_cost)
            
            # Expand neighbors
            for neighbor, distance in self.graph.get(current, {}).items():
                # Skip if already expanded
                if neighbor in expanded:
                    continue
                    
                new_cost = current_cost + distance
                
                # Only explore if better path found
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(frontier, (new_cost, neighbor))
        
        # No path found
        return (None, 0)