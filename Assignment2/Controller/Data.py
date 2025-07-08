from Model.Destination import Node

class sampleData:
    def __init__(self):
        self.locations = [
            Node("A", "Quảng trường trung tâm", 0, 0, "Quảng trường"),
            Node("B", "Khách sạn Hà Nội Luxury", 5, 0, "Khách sạn"),
            Node("C", "Cây xăng Petrolimex", 10, 0, "Cây xăng"),
            Node("D", "Công viên Hòa Bình", 0, 5, "Công viên"),
            Node("E", "ATM Vietcombank", 5, 5, "ATM"),
            Node("F", "Bệnh viện Bạch Mai", 10, 5, "Bệnh viện"),
            Node("G", "Nhà hàng Phở 24", 0, 10, "Nhà hàng"),
            Node("H", "Khách sạn Melia", 5, 10, "Khách sạn"),
            Node("I", "Trạm xe buýt Cầu Giấy", 10, 10, "Trạm xe buýt"),
            Node("J", "Cửa hàng Circle K", 15, 5, "Cửa hàng"),
            Node("K", "Sân bay Nội Bài", 15, 10, "Sân bay"),
            Node("L", "Ngã ba Láng - Nguyễn Trãi", 5, -5),
            Node("R1", "Ngã rẽ", 3, -1),
            Node("R2", "Ngã rẽ", 3.5, 5),
            Node("R3", "Ngã rẽ", 3, 3),
            Node("R6", "Ngã rẽ", 6, 2),
            Node("R4", "Ngã rẽ", 3, 7),
            Node("R5", "Ngã rẽ", 12, 4),
            Node("R7", "Ngã Tư Sở", 4.25, 2.6),
            Node("R8", "Ngã Tư", 7.5, 5),
            Node("R9", "Ngã Ba", 12, -2)
        ]

        self.roads = [
            # Trung tâm đến các điểm xung quanh
            ("R7", "R6", ["car", "motorbike"], False),
            ("R7", "B", ["car", "motorbike"], False),
            ("R7", "R3", ["car", "motorbike", "walking"], False),
            ("A", "R1", ["car", "motorbike", "walking"], False),
            ("R1", "B", ["car", "motorbike", "walking"], False),
            ("A", "D", ["car", "motorbike", "walking"], False),
            ("B", "C", ["car", "motorbike"], False),
            ("D", "R2", ["car", "motorbike", "walking"], False),
            ("R2", "E", ["car", "motorbike", "walking"], False),
            ("B", "E", ["car", "motorbike"], False),
            ("C", "F", ["car", "motorbike"], False),
            ("E", "F", ["car", "motorbike", "walking"], False),
            # Hàng ngang phía trên
            ("D", "G", ["car", "motorbike", "walking"], False),
            ("E", "H", ["car", "motorbike", "walking"], False),
            ("F", "I", ["car", "motorbike"], False),
            # Hàng ngang phía dưới
            ("B", "L", ["car", "motorbike"], False),
            # Hàng dọc bên phải
            ("C", "J", ["car", "motorbike"], False),
            ("F", "R5", ["car", "motorbike"], False),
            ("R5", "J", ["car", "motorbike"], False),
            ("J", "K", ["car"], False),
            ("I", "K", ["car"], False),
            # Các ngã rẽ tạo ngã tư/ngã ba
            ("E", "B", ["car", "motorbike"], False),      # Ngã tư E-B-D
            ("E", "H", ["car", "motorbike"], False),      # Ngã tư E-D-H
            ("H", "I", ["car", "motorbike"], False),      # Hướng từ công viên đến sân bay
            ("D", "G", ["car", "motorbike", "walking"], False),
            ("G", "H", ["car", "motorbike"], False),
            ("L", "A", ["car", "motorbike"], False),      # Ngã ba L nối vào trung tâm
            # Ngã rẽ chéo
            ("A", "R3", ["car", "motorbike", "walking"], False),
            ("R6", "R3", ["car", "motorbike", "walking"], False),
            ("R6", "I", ["car", "motorbike", "walking"], False),
            ("R4", "G", ["car", "motorbike"], False),
            # Tuyến đường mới theo comment
            ("F", "K", ["car"], False),                   # F nối với K
            ("R2", "R4", ["car", "motorbike", "walking"], False),  # R2 nối với R4
            ("R2", "R7", ["car", "motorbike"], False),    # R2 nối với R7
            ("R8", "I", ["car", "motorbike"], False),     # R8 nối với I
            ("R8", "R6", ["car", "motorbike"], False),    # R8 nối với R6
            ("R8", "E", ["car", "motorbike", "walking"], False),   # R8 nối với E
            ("R8", "F", ["car", "motorbike"], False),     # R8 nối với F
            ("R9", "C", ["car", "motorbike"], False),     # R9 nối với C
            ("R9", "L", ["car", "motorbike"], False),     # R9 nối với L
            ("R9", "J", ["car", "motorbike"], False)      # R9 nối với J
        ]

    def getData(self):
        return self.locations, self.roads