from Model.GraphModel import Graph
from Model.Destination import Node
from Model.Edges import Edge
from View.SystemView import View
from .Data import sampleData
from .logUsage import Logger

class Controller:
    def __init__(self):
        self.graph = Graph()
        self.view = View()
        self.data = sampleData()
        self.logger = Logger()  # Initialize logger
        self.initialize_data()

    def initialize_data(self):
        locations, roads = self.data.getData()
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
                self.path_to_multi_destinations()
            elif choice == '8':
                self.view.showMessage("Cảm ơn bạn đã sử dụng hệ thống!")
                break
            else:
                self.view.showMessage("Lựa chọn không hợp lệ!", True)
            
            if choice != '7':
                self.view.pressEnterToContinue()

    def handle_display_map(self):
        self.view.displayMap(self.graph)
        print("\n" + "="*40)
        self.view.displayRoads(self.graph)
        self.logger.log_display_map()  # Log display map action

    def handle_add_location(self):
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
        self.logger.log_add_location(location_data)  # Log add location action

    def handle_add_road(self):
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
        self.logger.log_add_road(road_data)  # Log add road action

    def handle_delete_location(self):
        location_id, error = self.view.getLocationToDelete(self.graph)
        
        if error:
            self.view.showMessage(error, True)
            return
        
        if self.graph.removeVertex(location_id):
            self.view.showMessage(f"Đã xóa địa điểm '{self.graph.getNodeById(location_id).Name}' thành công!")
            self.logger.log_delete_location(location_id)  # Log delete location action
        else:
            self.view.showMessage("Không thể xóa địa điểm!", True)

    def handle_find_path(self):
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
        self.logger.log_find_path(path_data, start.Name, end.Name, total_time)  # Log find path action

    def handle_find_nearby(self):
        search_data, error = self.view.getNearbySearchInput(self.graph)
        
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
            self.logger.log_find_nearby(search_data, selected_id, vehicle, total_time)  # Log find nearby action

    def handle_statistics(self):
        stats = self.graph.getStatistics()
        self.view.displayStatistics(stats)
        self.logger.log_statistics()  # Log statistics action

    def path_to_multi_destinations(self):
        path_data, error = self.view.getPathFindingInput(self.graph)
        
        if error:
            self.view.showMessage(error, True)
            return
        
        start = self.graph.getNodeById(path_data['start']) or self.graph.getNodeByName(path_data['start'])
        end = self.graph.getNodeById(path_data['end']) or self.graph.getNodeByName(path_data['end'])
        total_time = 0.0
        while True:
            if not start or not end:
                self.view.showMessage(f"Không tìm thấy điểm {'bắt đầu' if not start else 'kết thúc'}!", True)
                return
            
            result = self.graph.dijkstra(start, end, path_data['vehicle'], path_data['metric'])
            if len(result) < 1:
                print("\nPhương tiện vừa rồi không tìm thấy đường đi, vui lòng chọn phương tiện khác:")
                print("1. Xe máy (mặc định)")
                print("2. Ô tô")
                print("3. Đi bộ")
                
                vehicle_choice_input = input("Chọn phương tiện (1-3): ").strip()
                vehicles = {"1": "motorbike", "2": "car", "3": "walking"}
                newVehicle = vehicles.get(vehicle_choice_input, "motorbike")
                path_data['vehicle'] = newVehicle
                result = self.graph.dijkstra(start, end, path_data['vehicle'], path_data['metric'])
            if result:
                nodes = list(result.keys())
                for i in range(1, len(nodes)):
                    if nodes[i] in self.graph.adjList[nodes[i-1]] and self.graph.adjList[nodes[i-1]][nodes[i]].canTraverse(path_data['vehicle']):
                        total_time += self.graph.adjList[nodes[i-1]][nodes[i]].getTravelTime(path_data['vehicle'])
            
            self.view.displayPathResult(result, start.Name, end.Name, path_data['vehicle'], total_time)
            self.logger.log_find_path(path_data, start.Name, end.Name, total_time)  # Log find path action
            start = end
            continue_choice = self.view.getContinueChoice()
            if continue_choice.lower() != 'y':
                self.view.showMessage(f"Tổng thời gian hành trình: {self.view.formatTime(total_time)}")
                break
            else:
                while True:
                    end = input("\nNhập vị trí cần đến (ID hoặc tên, để trống để hủy): ").strip()
                    if not end:
                        return None, "Đã hủy thao tác tìm địa điểm."
                    
                    # Kiểm tra tính hợp lệ của end
                    end = self.graph.getNodeById(end) or self.graph.getNodeByName(end)
                    if end:
                        break
                    print("Vị trí không tồn tại! Vui lòng nhập lại.")

