from Model.GraphModel import Graph
from Model.Destination import Node
from Model.Edges import Edge
from View.SystemView import View

class Controller:
    def __init__(self):
        self.graph = Graph()
        self.view = View()
        self.initialize_data()

    def initialize_data(self):
        """Khởi tạo dữ liệu mẫu"""
        locations = [
            Node("A", "Trung tâm thành phố", 0, 0),
            Node("B", "Bệnh viện Bạch Mai", 2, 1, 'Bệnh viện'),
            Node("C", "Cây xăng Shell", 1, 3, 'Cây xăng'),
            Node("D", "Khách sạn Hilton", 4, 2, 'Khách sạn'),
            Node("E", "ATM Vietcombank", 3, 4, 'ATM'),
            Node("F", "Nhà hàng Golden Dragon", 5, 1, 'Nhà hàng'),
            Node("G", "Cửa hàng tiện lợi VinMart", 6, 3, 'Cửa hàng tiện lợi'),
            Node("H", "Trường Đại học Bách Khoa", 2, 5),
            Node("I", "Công viên Thống Nhất", 3, 0, 'Công viên'),
            Node("J", "Trạm xe buýt Mỹ Đình", 7, 2, 'Trạm xe buýt'),
            Node("K", "Sân bay Nội Bài", 8, 4, 'Sân bay'),
            Node("L", "Bến xe Giáp Bát", 1, 6, 'Trạm xe buýt'),
            Node("M", "Trung tâm thương mại Vincom", 4, 5),
            Node("N", "Cây xăng Petrolimex", 2, 2, 'Cây xăng'),
            Node("O", "Cây xăng Total", 3, 3, 'Cây xăng'),
            Node("P", "Cây xăng Mobil", 5, 4, 'Cây xăng')
        ]

        roads = [
            ("A", "B", ["car", "motorbike", "walking"]),
            ("A", "C", ["car", "motorbike", "walking"]),
            ("B", "C", ["car", "motorbike", "walking"]),
            ("B", "D", ["car", "motorbike"]),
            ("C", "D", ["car", "motorbike"]),
            ("D", "E", ["car", "motorbike", "walking"]),
            ("E", "F", ["car", "motorbike", "walking"]),
            ("F", "G", ["car", "motorbike"]),
            ("G", "H", ["car", "motorbike", "walking"]),
            ("H", "I", ["walking", 'motorbike']),
            ("I", "J", ["car", "motorbike"]),
            ("J", "K", ["car", "motorbike"]),
            ("K", "L", ["car", "motorbike", "walking"]),
            ("L", "M", ["car", "motorbike", "walking"]),
            ("M", "N", ["car", "motorbike", "walking"]),
            ("N", "O", ["car", "motorbike", "walking"]),
            ("O", "P", ["car", "motorbike", "walking"])
        ]

        for location in locations:
            self.graph.addVertex(location)

        for road in roads:
            u = self.graph.getNodeById(road[0])
            v = self.graph.getNodeById(road[1])
            e = Edge(u, v, road[2])
            self.graph.addEdge(e)

    def run(self):
        """Chạy chương trình chính"""
        while True:
            choice = self.view.displayMenu()
            
            if choice == '0':
                self.handle_display_map()
            elif choice == '1':
                self.handle_add_location()
            elif choice == '2':
                self.handle_add_road()
            elif choice == '3':
                self.handle_delete_location()
            elif choice == '4':
                self.handle_find_path()
            elif choice == '5':
                self.handle_find_nearby()
            elif choice == '6':
                self.handle_statistics()
            elif choice == '7':
                self.view.showMessage("Cảm ơn bạn đã sử dụng hệ thống!")
                break
            else:
                self.view.showMessage("Lựa chọn không hợp lệ!", True)
            
            if choice != '7':
                self.view.pressEnterToContinue()

    def handle_display_map(self):
        """Xử lý hiển thị bản đồ"""
        self.view.displayMap(self.graph)
        print("\n" + "="*40)
        self.view.displayRoads(self.graph)

    def handle_add_location(self):
        """Xử lý thêm địa điểm mới"""
        location_data, error = self.view.getNewLocationInput()
        
        if error:
            self.view.showMessage(error, True)
            return
        
        if location_data['id'] in self.graph.nodes:
            self.view.showMessage("ID địa điểm đã tồn tại!", True)
            return
        
        new_node = Node(
            location_data['id'],
            location_data['name'],
            location_data['x'],
            location_data['y'],
            location_data['type']
        )
        
        self.graph.addVertex(new_node)
        self.view.showMessage(f"Đã thêm địa điểm '{location_data['name']}' thành công!")

    def handle_add_road(self):
        """Xử lý thêm tuyến đường mới"""
        road_data, error = self.view.getNewRoadInput(self.graph)
        
        if error:
            self.view.showMessage(error, True)
            return
        
        from_node = self.graph.getNodeById(road_data['from_id'])
        to_node = self.graph.getNodeById(road_data['to_id'])
        
        if (from_node, to_node) in self.graph.edges:
            self.view.showMessage("Tuyến đường đã tồn tại!", True)
            return
        
        edge = Edge(from_node, to_node, road_data['allowed_vehicles'], road_data['is_oneway'])
        self.graph.addEdge(edge)
        self.view.showMessage("Đã thêm tuyến đường thành công!")

    def handle_delete_location(self):
        """Xử lý xóa địa điểm"""
        location_id, error = self.view.getLocationToDelete(self.graph)
        
        if error:
            self.view.showMessage(error, True)
            return
        
        if self.graph.removeVertex(location_id):
            self.view.showMessage(f"Đã xóa địa điểm '{self.graph.getNodeById(location_id).Name}' thành công!")
        else:
            self.view.showMessage("Không thể xóa địa điểm!", True)

    def handle_find_path(self):
        """Xử lý tìm đường đi ngắn nhất"""
        path_data, error = self.view.getPathFindingInput(self.graph)
        
        if error:
            self.view.showMessage(error, True)
            return
        
        start = self.graph.getNodeById(path_data['start']) or self.graph.getNodeByName(path_data['start'])
        end = self.graph.getNodeById(path_data['end']) or self.graph.getNodeByName(path_data['end'])
        
        if not start or not end:
            self.view.showMessage(f"Không tìm thấy điểm {'bắt đầu' if not start else 'kết thúc'}!", True)
            return
        
        result = self.graph.dijkstra(start, end, path_data['vehicle'], path_data['metric'])
        total_time = 0.0
        if result:
            nodes = list(result.keys())
            for i in range(1, len(nodes)):
                if nodes[i] in self.graph.adjList[nodes[i-1]] and self.graph.adjList[nodes[i-1]][nodes[i]].canTraverse(path_data['vehicle']):
                    total_time += self.graph.adjList[nodes[i-1]][nodes[i]].getTravelTime(path_data['vehicle'])
        
        self.view.displayPathResult(result, start.Name, end.Name, path_data['vehicle'], total_time)

    def handle_find_nearby(self):
        """Xử lý tìm địa điểm gần đây"""
        search_data, error = self.view.getNearbySearchInput()
        
        if error:
            self.view.showMessage(error, True)
            return
        
        results = self.graph.BFS(search_data['start'], search_data['location_type'], search_data['number'])
        selected_id = self.view.displayNearbyResults(results, search_data['location_type'])
        
        if selected_id:
            vehicle = self.view.getVehicleChoice()
            result = self.graph.dijkstra(selected_id, search_data['start'], vehicle)
            total_time = 0.0
            if result:
                nodes = list(result.keys())
                for i in range(1, len(nodes)):
                    if nodes[i] in self.graph.adjList[nodes[i-1]] and self.graph.adjList[nodes[i-1]][nodes[i]].canTraverse(vehicle):
                        total_time += self.graph.adjList[nodes[i-1]][nodes[i]].getTravelTime(vehicle)
            
            start_node = self.graph.getNodeById(search_data['start']) or self.graph.getNodeByName(search_data['start'])
            end_node = self.graph.getNodeById(selected_id)
            self.view.displayPathResult(result, start_node.Name if start_node else search_data['start'], end_node.Name if end_node else selected_id, vehicle, total_time)

    def handle_statistics(self):
        """Xử lý thống kê hệ thống"""
        stats = self.graph.getStatistics()
        self.view.displayStatistics(stats)