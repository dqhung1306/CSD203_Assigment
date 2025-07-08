from .Edges import Edge
from .MyQueue import My_Queue
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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

    def removeVertex(self, node_id):
        node = self.getNodeById(node_id)
        if not node:
            return False
        
        edges_to_remove = [(u, v) for u, v in self.edges.keys() if u == node or v == node]
        for edge_key in edges_to_remove:
            del self.edges[edge_key]
        
        if node in self.adjList:
            del self.adjList[node]
        for u in self.adjList:
            if node in self.adjList[u]:
                del self.adjList[u][node]
        
        if node_id in self.nodes:
            del self.nodes[node_id]
        
        return True

    def dijkstra(self, start, end, vehicle_type="motorbike", metric="distance"):
        start = self.getNodeById(start) if start in self.nodes else self.getNodeByName(start)
        end = self.getNodeById(end) if end in self.nodes else self.getNodeByName(end)
        if not start or not end:
            return {}
        
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
 
        if end not in prev or distant[end] == float('inf'):
            return {}

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = prev.get(current) 
        
        result = {}
        for u in reversed(path):
            result[u] = distant[u]
        
        return result

    def getNodeById(self, node_id):
        return self.nodes.get(node_id)

    def getNodeByName(self, name):
        for node in self.nodes.values():
            if node.Name.lower() == name.Name.lower():
                return node
        return None
    
    def BFS(self, start, locationType, number=1):
        start_node = self.getNodeById(start) if start in self.nodes else self.getNodeByName(start)
        if not start_node:
            return []
        
        store = []
        visited = set()
        queue = [start_node]
        visited.add(start_node)

        while queue:
            current = queue.pop(0)
            if current.locationType.upper() == locationType.upper():
                minDist = list(self.dijkstra(start, current).values())[-1]
                store.append((current, minDist))
                if len(store) >= int(number):
                    return store
            for neighbor in self.adjList[current].keys():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return store
    def getStatistics(self):
        total_locations = len(self.nodes)
        total_roads = len(self.edges)
        
        total_distance = 0.0
        location_types = {}
        vehicle_support = {'car': 0, 'motorbike': 0, 'walking': 0}
        
        processed_edges = set()
        for (u, v), edge in self.edges.items():
            if (v, u) not in processed_edges:  # Tránh tính trùng cho đường hai chiều
                total_distance += edge.fromNode.distanceTo(edge.toNode)
                processed_edges.add((u, v))
                if not edge.isOneWay:
                    processed_edges.add((v, u))
                for vehicle in vehicle_support:
                    if edge.canTraverse(vehicle):
                        vehicle_support[vehicle] += 1
        
        for node in self.nodes.values():
            ltype = node.locationType if node.locationType else "Khác"
            location_types[ltype] = location_types.get(ltype, 0) + 1
        
        return {
            'total_locations': total_locations,
            'total_roads': total_roads,
            'total_distance': total_distance,
            'location_types': location_types,
            'vehicle_support': vehicle_support
        }


    def draw_graph(self):

        plt.figure(figsize=(15, 8))
        for start_node, neighbors in self.adjList.items():
            for end_node, edge in neighbors.items():
                x_values = [start_node.x, end_node.x]
                y_values = [start_node.y, end_node.y]
                plt.plot(x_values, y_values, 'k-', lw=1)

        types = {}
        for node in self.adjList.keys():
            if node.locationType not in types:
                types[node.locationType] = []
            types[node.locationType].append(node)

        colors = {
            "Bệnh viện": "red",
            "Cây xăng": "blue",
            "Khách sạn": "green",
            "Công viên": "purple",
            "ATM": "orange",
            "Nhà hàng": "cyan",
            "Cửa hàng tiện lợi": "magenta",
            "Trạm xe buýt": "yellow",
            "Sân bay": "black",
            "Khác": "gray"
        }
        unique_types = list(types.keys())
        if len(unique_types) > len(colors):
            cmap = cm.get_cmap('tab10')
            for i, type_name in enumerate(unique_types):
                if type_name not in colors:
                    colors[type_name] = cmap(i % 10)

        for type_name, nodes in types.items():
            if nodes: 
                x = [node.x for node in nodes]
                y = [node.y for node in nodes]
                plt.scatter(x, y, s=100, c=colors[type_name], label=type_name)

        for node in self.adjList.keys():
            plt.text(node.x, node.y, f"{node.Name}", fontsize=8)

        plt.title("Bản đồ khu phố")
        plt.xlabel("Tọa độ X")
        plt.ylabel("Tọa độ Y")
        plt.grid(True)
        plt.legend()
        plt.show()