class DFSAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.expanded_nodes = 0
    
    def search(self, start, goal):
        """
        Search for a path from start to goal using DFS.
        Returns: (path, cost) tuple
        """
        self.expanded_nodes = 0
        path = []
        
        result_path, total_cost = self._dfs_recursive(start, goal, path, 0)
        
        return result_path, total_cost
    
    def _dfs_recursive(self, current, goal, path, cost):
        """Recursive DFS algorithm"""
        path.append(current)
        self.expanded_nodes += 1
        
        if current == goal:
            return (path.copy(), cost)
        
        # Explore neighbors in sorted order
        neighbors = sorted(self.graph.get(current, {}).keys())
        
        for neighbor in neighbors:
            if neighbor not in path:
                edge_cost = self.graph[current][neighbor]
                result, total_cost = self._dfs_recursive(
                    neighbor, goal, path, cost + edge_cost
                )
                if result:
                    return (result, total_cost)
        
        # Backtrack if the path doesn't work
        path.pop()
        return (None, 0)