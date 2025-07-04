from tabulate import tabulate
from Model.GraphModel import Graph

class View:
    def displayMenu(self):
        print("\n" + "="*50)
        print("HỆ THỐNG ĐIỀU HƯỚNG THÔNG MINH")
        print("="*50)
        print("0. Hiển thị bản đồ")
        print("1. Thêm địa điểm mới")
        print("2. Thêm tuyến đường mới")
        print("3. Xóa địa điểm")
        print("4. Tìm đường đi ngắn nhất từ vị trí hiện tại đến địa điểm chỉ định")
        print("5. Tìm các địa điểm công cộng gần đây")
        print("6. Thống kê hệ thống")
        print("7. Tìm đường đi qua nhiều địa điểm chỉ định")
        print("8. Thoát")
        print("="*50)
        return input("Chọn chức năng (0-8): ").strip()

    def displayMap(self, graph):
        """Hiển thị bản đồ dưới dạng bảng"""
        print("\n" + "="*80)
        print("BẢNG ĐỒ CÁC ĐỊA ĐIỂM")
        print("="*80)
        
        if not graph.nodes:
            print("Chưa có địa điểm nào trong hệ thống!")
            return
            
        # Tạo data cho bảng
        data = []
        for node in graph.nodes.values():
            data.append([
                node.Id,
                node.Name,
                f"({node.x}, {node.y})",
                node.locationType
            ])
        
        headers = ["ID", "Tên địa điểm", "Tọa độ", "Loại"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
        
        print(f"\nTổng số địa điểm: {len(graph.nodes)}")

    def displayRoads(self, graph):
        print("\n" + "="*100)
        print("DANH SÁCH CÁC TUYẾN ĐƯỜNG")
        print("="*100)
        
        if not graph.edges:
            print("Chưa có tuyến đường nào!")
            return
        data = []
        processed_edges = set()
        for (start, end), edge in graph.edges.items():
            if (end, start) not in processed_edges:  # Tránh hiển thị trùng cho đường hai chiều
                vehicles = ", ".join([self.vehicleType(v) for v in edge.allowedVehicles])
                data.append([
                    f"{start.Id}-{end.Id}",
                    start.Name,
                    end.Name,
                    f"{start.distanceTo(end):.2f} km",
                    vehicles,
                    "Một chiều" if edge.isOneWay else "Hai chiều"
                ])
                processed_edges.add((start, end))
                if not edge.isOneWay:
                    processed_edges.add((end, start))
        
        headers = ["ID Tuyến", "Điểm bắt đầu", "Điểm đến", "Khoảng cách", "Phương tiện", "Loại đường"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
        
        print(f"\nTổng số tuyến đường: {len(processed_edges)}")

    def getNewLocationInput(self):
        """Lấy thông tin địa điểm mới từ người dùng"""
        print("\nTHÊM ĐỊA ĐIỂM MỚI")
        print("-" * 30)
        
        location_id = input("Nhập ID địa điểm: ").strip().upper()
        name = input("Nhập tên địa điểm: ").strip()
        
        x_input = input("Nhập tọa độ X: ").strip()
        y_input = input("Nhập tọa độ Y: ").strip()
        
        if not x_input.replace(".", "").replace("-", "").isdigit() or not y_input.replace(".", "").replace("-", "").isdigit():
            return None, "Tọa độ phải là số!"
        
        x = float(x_input)
        y = float(y_input)
        
        print("\nChọn loại địa điểm:")
        location_types = [
            "Bệnh viện", "Cây xăng", "Khách sạn", "ATM", 
            "Nhà hàng", "Cửa hàng tiện lợi", "Công viên", 
            "Trạm xe buýt", "Sân bay", "Khác"
        ]
        
        for i, ltype in enumerate(location_types, 1):
            print(f"{i}. {ltype}")
        
        choice_input = input("Chọn loại (1-10): ").strip()
        if choice_input.isdigit():
            choice = int(choice_input) - 1
            location_type = location_types[choice] if 0 <= choice < len(location_types) else "Khác"
        else:
            location_type = "Khác"
        
        return {
            'id': location_id,
            'name': name,
            'x': x,
            'y': y,
            'type': location_type
        }, None

    def getNewRoadInput(self, graph, is_one_way = False):
        """Lấy thông tin tuyến đường mới"""
        print("\nTHÊM TUYẾN ĐƯỜNG MỚI")
        print("-" * 30)
        
        # Hiển thị danh sách địa điểm có sẵn
        print("Danh sách địa điểm hiện có:")
        for node_id, node in graph.nodes.items():
            print(f"  {node_id}: {node.Name}")
        
        from_id = input("\nNhập ID điểm bắt đầu: ").strip().upper()
        to_id = input("Nhập ID điểm kết thúc: ").strip().upper()
        
        if from_id not in graph.nodes or to_id not in graph.nodes:
            return None, "Một hoặc cả hai địa điểm không tồn tại!"
        
        print("\nChọn phương tiện được phép:")
        print("1. Tất cả phương tiện (Ô tô, Xe máy, Đi bộ)")
        print("2. Chỉ Ô tô và Xe máy")
        print("3. Chỉ Xe máy và Đi bộ")
        print("4. Chỉ Đi bộ")
        
        vehicle_choice_input = input("Chọn (1-4): ").strip()
        vehicle_options = {
            "1": ["car", "motorbike", "walking"],
            "2": ["car", "motorbike"],
            "3": ["motorbike", "walking"],
            "4": ["walking"]
        }
        allowed_vehicles = vehicle_options.get(vehicle_choice_input, ["car", "motorbike", "walking"])
        
        is_oneway = input("Đường một chiều? (y/n): ").strip().lower() == 'y'
        
        return {
            'from_id': from_id,
            'to_id': to_id,
            'allowed_vehicles': allowed_vehicles,
            'is_oneway': is_oneway
        }, None

    def getLocationToDelete(self, graph):
        """Lấy thông tin địa điểm cần xóa"""
        print("\nXÓA ĐỊA ĐIỂM")
        print("-" * 20)
        
        # Hiển thị danh sách địa điểm
        print("Danh sách địa điểm hiện có:")
        for node_id, node in graph.nodes.items():
            print(f"  {node_id}: {node.Name}")
        
        location_id = input("\nNhập ID địa điểm cần xóa: ").strip().upper()
        
        if location_id not in graph.nodes:
            return None, "Địa điểm không tồn tại!"
        
        confirm = input(f"Bạn có chắc muốn xóa '{graph.nodes[location_id].Name}'? (y/n): ").strip().lower()
        if confirm != 'y':
            return None, "Đã hủy thao tác xóa."
        
        return location_id, None

    def getPathFindingInput(self, graph):
        """Lấy thông tin tìm đường"""
        print("\nTÌM ĐƯỜNG ĐI NGẮN NHẤT")
        print("-" * 30)
        
        # Hiển thị danh sách địa điểm
        print("Danh sách địa điểm:")
        for node_id, node in graph.nodes.items():
            print(f"  {node_id}: {node.Name}")
        start, end = None, None 
        while True:
            start = input("\nNhập vị trí hiện tại (ID hoặc tên, để trống để hủy): ").strip()
            if not start:
                return None, "Đã hủy thao tác tìm địa điểm."
            
            # Kiểm tra tính hợp lệ của start
            start_node = graph.getNodeById(start) or graph.getNodeByName(start)
            if start_node:
                break
            print("Vị trí không tồn tại! Vui lòng nhập lại.")
        while True:
            end = input("\nNhập vị trí cần đến (ID hoặc tên, để trống để hủy): ").strip()
            if not end:
                return None, "Đã hủy thao tác tìm địa điểm."
            
            # Kiểm tra tính hợp lệ của end
            end_node = graph.getNodeById(end) or graph.getNodeByName(end)
            if end_node:
                break
            print("Vị trí không tồn tại! Vui lòng nhập lại.")
        
        print("\nChọn phương tiện:")
        print("1. Xe máy (mặc định)")
        print("2. Ô tô")
        print("3. Đi bộ")
        
        vehicle_choice_input = input("Chọn phương tiện (1-3): ").strip()
        vehicles = {"1": "motorbike", "2": "car", "3": "walking"}
        vehicle = vehicles.get(vehicle_choice_input, "motorbike")
        
        print("\nChọn tiêu chí tối ưu:")
        print("1. Khoảng cách ngắn nhất")
        print("2. Thời gian nhanh nhất")
        
       

        metric_choice_input = input("Chọn tiêu chí (1-2): ").strip()
        metric = "distance" if metric_choice_input == "1" else "time"
        
        return {
            'start': start,
            'end': end,
            'vehicle': vehicle,
            'metric': metric
        }, None

    def getNearbySearchInput(self, graph):
        """Lấy thông tin tìm địa điểm gần đây"""
        print("\nTÌM ĐỊA ĐIỂM GẦN ĐÂY")
        print("-" * 30)
        while True:
            start = input("\nNhập vị trí hiện tại (ID hoặc tên, để trống để hủy): ").strip()
            if not start:
                return None, "Đã hủy thao tác tìm địa điểm."
            
            # Kiểm tra tính hợp lệ của start
            start_node = graph.getNodeById(start) or graph.getNodeByName(start)
            if start_node:
                break
            print("Vị trí không tồn tại! Vui lòng nhập lại.")
        print("\nChọn loại địa điểm cần tìm:")
        location_types = [
            "Bệnh viện", "Cây xăng", "Khách sạn", "ATM", 
            "Nhà hàng", "Cửa hàng tiện lợi", "Công viên", 
            "Trạm xe buýt", "Sân bay"
        ]
        
        for i, ltype in enumerate(location_types, 1):
            print(f"{i}. {ltype}")
        
        choice_input = input("Chọn loại (1-9): ").strip()
        if choice_input.isdigit():
            choice = int(choice_input) - 1
            location_type = location_types[choice] if 0 <= choice < len(location_types) else location_types[0]
        else:
            location_type = location_types[0]
        
        num_input = input("Số lượng địa điểm cần tìm: ").strip()
        if num_input.isdigit():
            num = int(num_input)
            num = max(1, min(10, num))  # Giới hạn từ 1-10
        else:
            num = 3
        
        return {
            'start': start,
            'location_type': location_type,
            'number': num
        }, None

    def displayPathResult(self, result, start_name, end_name, vehicle, total_time=0):
        """Hiển thị kết quả tìm đường"""
        print("\n" + "="*60)
        print("KẾT QUẢ TÌM ĐƯỜNG")
        print("="*60)
        
        if not result:
            print(f"Không có đường đi từ {start_name} đến {end_name} bằng {self.vehicleType(vehicle)}")
            return
        
        print(f"Đường đi từ {start_name} đến {end_name} bằng {self.vehicleType(vehicle)}:")
        print("-" * 60)
        
        nodes = list(result.keys())
        distances = list(result.values())
        
        for i, (node, distance) in enumerate(zip(nodes, distances)):
            if i == 0:
                print(f"Bắt đầu tại: {node.Name}")
            elif i == len(nodes) - 1:
                segment_distance = distance - distances[i-1]
                print(f"-> Đi {segment_distance:.2f} km đến: {node.Name}")
                print(f"Đến đích sau tổng cộng: {distance:.2f} km")
            else:
                segment_distance = distance - distances[i-1]
                prev_node = nodes[i-2] if i >= 2 else nodes[i-1]
                action = nodes[i-1].navigate(prev_node, node)
                print(f"-> Đi {segment_distance:.2f} km đến: {node.Name}, sau đó {action}")
        
        if total_time > 0:
            print(f"\nTổng thời gian ước tính: {total_time:.2f} phút")
        
        print("="*60)

    def displayNearbyResults(self, results, location_type):
        """Hiển thị kết quả tìm địa điểm gần đây"""
        print(f"\nCác {location_type} gần đây:")
        print("-" * 40)
        
        if not results:
            print(f"Không tìm thấy {location_type} nào!")
            return None
        
        for i, node in enumerate(results, 1):
            print(f"{i}. {node.Name} - {node}")
        
        choice_input = input(f"\nChọn {location_type} để đi đến (số thứ tự): ").strip()
        if choice_input.isdigit():
            choice = int(choice_input) - 1
            if 0 <= choice < len(results):
                return results[choice].Id
        
        return None

    def getVehicleChoice(self):
        """Lấy lựa chọn phương tiện"""
        print("\nChọn phương tiện di chuyển:")
        print("1. Xe máy")
        print("2. Ô tô") 
        print("3. Đi bộ")
        
        choice_input = input("Chọn phương tiện (1-3): ").strip()
        vehicles = {"1": "motorbike", "2": "car", "3": "walking"}
        return vehicles.get(choice_input, "motorbike")

    def displayStatistics(self, stats):
        """Hiển thị thống kê hệ thống"""
        print("\n" + "="*50)
        print("THỐNG KÊ HỆ THỐNG")
        print("="*50)
        
        print(f"Tổng số địa điểm: {stats['total_locations']}")
        print(f"Tổng số tuyến đường: {stats['total_roads']}")
        print(f"Tổng độ dài đường: {stats['total_distance']:.2f} km")
        
        print(f"\nPhân loại địa điểm:")
        for loc_type, count in stats['location_types'].items():
            print(f"   {loc_type}: {count}")
        
        print(f"\nPhương tiện được hỗ trợ:")
        for vehicle, count in stats['vehicle_support'].items():
            print(f"   {self.vehicleType(vehicle)}: {count} tuyến đường")

    def vehicleType(self, vehicle):
        """Chuyển đổi tên phương tiện sang tiếng Việt"""
        vehicle_names = {
            'motorbike': 'Xe máy',
            'car': 'Ô tô',
            'walking': 'Đi bộ'
        }
        return vehicle_names.get(vehicle, 'Không xác định')

    def showMessage(self, message, is_error=False):
        """Hiển thị thông báo"""
        icon = "ERROR" if is_error else "SUCCESS"
        print(f"\n[{icon}] {message}")

    def pressEnterToContinue(self):
        """Đợi người dùng nhấn Enter để tiếp tục"""
        input("\nNhấn Enter để tiếp tục...")

    def getContinueChoice(self):
        """Hỏi người dùng có muốn tiếp tục đến điểm khác không"""
        print("\nBạn có muốn tiếp tục đến một địa điểm khác không?")
        return input("Nhập 'y' để tiếp tục, bất kỳ phím nào khác để dừng: ").strip().lower()
    def formatTime(self, minutes):
        """Định dạng thời gian từ phút sang giờ và phút nếu lớn hơn 60 phút"""
        if minutes > 60:
            hours = int(minutes // 60)
            remaining_minutes = int(minutes % 60)
            return f"{hours} giờ {remaining_minutes} phút" if remaining_minutes > 0 else f"{hours} giờ"
        return f"{minutes:.2f} phút"