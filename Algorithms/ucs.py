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
        self.expanded_nodes = 0
        
        # Priority queue: (cost, current_city, path)
        frontier = [(0, start, [start])]
        visited = set()

        while frontier:
            cost, city, path = heapq.heappop(frontier)

            # Skip if already visited
            if city in visited:
                continue
            
            visited.add(city)
            self.expanded_nodes += 1

            # Goal check
            if city == goal:
                return (path, cost)

            # Expand neighbors
            for neighbor, distance in self.graph.get(city, {}).items():
                if neighbor not in visited and distance >= 0:
                    new_cost = cost + distance
                    new_path = path + [neighbor]
                    heapq.heappush(frontier, (new_cost, neighbor, new_path))

        # No path found
        return (None, 0)