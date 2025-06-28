from Model.GraphModel import Graph
from Model.Destination import Node
from Model.Edges import Edge

def findPathById(startId, endId, vehicle = 'motorbike'):
    start = graph.getNodeById(startId)
    end = graph.getNodeById(endId)
    result = graph.djikstra(start, end)
    prev = None
    prevdistance = 0.0
    idx = 0
    totalTime = 0
    for node, distance in result.items():
        if idx == 0:
            print(f"Bắt đầu tại {node.Name}")
        elif idx == len(result) - 1:
            print(f"-> Đi {distance - prevdistance:.2f} km đến {node.Name}")
            print(f"Đến {node.Name} sau {distance:.2f} km")
            e = graph.edges.get((prev, node))
            if e:
                totalTime += e.travelTimes[vehicle]
        else:
            action = prev.navigate(node)
            print(f"-> Đi {distance - prevdistance:.2f} km đến {node.Name} sau đó {action}")
            e = graph.edges.get((prev, node))
            if e:
                totalTime += e.travelTimes[vehicle]
        idx += 1
        prev = node
        prevdistance = distance
    print(f"Tổng thời gian: {totalTime:.2f} phút")
if __name__ == "__main__":
    graph = Graph()
    locations = [
        Node("A", "Trung tâm thành phố", 0, 0),
        Node("B", "Bệnh viện Bạch Mai", 2, 1),
        Node("C", "Cây xăng Shell", 1, 3),
        Node("D", "Khách sạn Hilton", 4, 2),
        Node("E", "ATM Vietcombank", 3, 4),
        Node("F", "Nhà hàng Golden Dragon", 5, 1),
        Node("G", "Cửa hàng tiện lợi VinMart", 6, 3),
        Node("H", "Trường Đại học Bách Khoa", 2, 5),
        Node("I", "Công viên Thống Nhất", 3, 0),
        Node("J", "Trạm xe buýt Mỹ Đình", 7, 2),
        Node("K", "Sân bay Nội Bài", 8, 4),
        Node("L", "Bến xe Giáp Bát", 1, 6),
        Node("M", "Trung tâm thương mại Vincom", 4, 5),
        Node("N", "Cây xăng Petrolimex", 2, 2),
        Node("O", "Cây xăng Total", 3, 3),
        Node("P", "Cây xăng Mobil", 5, 4)
    ]
    roads = [
        ("A", "B", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("A", "C", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("B", "C", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("B", "D", {"isOneWay": False, "allowedVehicles": ["car", "motorbike"]}),
        ("C", "D", {"isOneWay": False, "allowedVehicles": ["car", "motorbike"]}),
        ("D", "E", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("E", "F", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("F", "G", {"isOneWay": False, "allowedVehicles": ["car", "motorbike"]}),
        ("G", "H", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("H", "I", {"isOneWay": False, "allowedVehicles": ["walking"]}),
        ("I", "J", {"isOneWay": False, "allowedVehicles": ["car", "motorbike"]}),
        ("J", "K", {"isOneWay": False, "allowedVehicles": ["car", "motorbike"]}),
        ("K", "L", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("L", "M", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("M", "N", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("N", "O", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]}),
        ("O", "P", {"isOneWay": False, "allowedVehicles": ["car", "motorbike", "walking"]})
    ]
    for location in locations:
        graph.addVertex(location)
    for road in roads:
        u = graph.getNodeById(road[0])
        v = graph.getNodeById(road[1])
        #print (u, v) 
        e = Edge(u, v)
        graph.addEdge(e)
    findPathById('A', 'K')
    