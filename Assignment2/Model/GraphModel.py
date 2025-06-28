from .Edges import Edge
from .MyQueue import My_Queue

class Graph:
    def __init__(self):
        self.adjList = {} 
        self.edges = {}   
        self.nodes = {}   

    def addVertex(self, v):
        if v.Id not in self.nodes:
            self.nodes[v.Id] = v
        if v not in self.adjList:
            self.adjList[v] = {}

    def addEdge(self, edge: Edge):
        start = edge.fromNode
        end = edge.toNode
        
        for node in (start, end):
            if node.Id not in self.nodes:
                self.addVertex(node)

        if start not in self.adjList:
            self.adjList[start] = {}
        if end not in self.adjList:
            self.adjList[end] = {}

        self.adjList[start][end] = edge
        
        if not edge.isOneWay:
            self.adjList[end][start] = edge

        self.edges[(start, end)] = edge
        if not edge.isOneWay:
            self.edges[(end, start)] = edge

    def djikstra(self, start, end, vehicle_type="motorbike", metric="distance"):
        visited = []
        prev = {}
        distant = {}
        myQueue = My_Queue()
        myQueue.EnQueue(start)
        
        for v in self.adjList.keys():
            distant[v] = float('inf')
        distant[start] = 0
        prev[start] = None

        while not myQueue.isEmpty():
            current = myQueue.DeQueue()
            if current not in visited:
                visited.append(current)
                for vertex, edge in self.adjList[current].items():
                    if edge.canTraverse(vehicle_type): 
                        weight = edge.getWeight(vehicle_type, metric)
                        if weight != float('inf') and distant[current] + weight < distant[vertex]:
                            distant[vertex] = distant[current] + weight
                            prev[vertex] = current
                            myQueue.EnQueue(vertex)

        path = []
        while end is not None:
            path.append(end)
            end = prev[end]
        
        result = {}
        for u in reversed(path):
            result[u] = distant[u]
        
        if distant[path[0]] == float('inf'):  # No valid path found
            return {}
        
        return result

    def getNodeById(self, node_id):
        return self.nodes.get(node_id)

    def getNodeByName(self, name):
        for node in self.nodes.values():
            if node.Name.lower() == name.lower():
                return node
        return None