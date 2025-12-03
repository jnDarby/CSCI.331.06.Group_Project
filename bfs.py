from collections import deque

class BFSAlgorithm:

    def __init__(self, graph):
        self.graph = graph
        self.expanded_nodes = 0

    def search(self, start, goal):
        
        visited = set([start])
        queue = deque([start]) #initialize queue with start node
        parent = {start: None}
        visited.add(start)

        while queue:
            
            current_node = queue.popleft() 
            self.expanded_nodes +=1
            if current_node == goal:   #reconstruct
                path = []
                cost = 0
                while current_node != None:
                    path.append(current_node)
                    current_node = parent[current_node]
                path.reverse()
                for i in range(len(path)-1):
                    cost += self.graph[path[i]][path[i+1]]
                return path,cost
            
            #add unvisited neighbors to queue
            for neighbor, distance in self.graph.get(current_node, {}).items():    
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_node
                    queue.append(neighbor)


