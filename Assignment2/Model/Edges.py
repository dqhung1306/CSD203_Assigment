from Model.Destination import Node
from Model.Vehicles import Car, Motorbike, Walking

class Edge:
    def __init__(self, from_node: Node, to_node: Node, allowedVehicles = None, isOneWay=False, isBlocked=False):
        self.fromNode = from_node
        self.toNode = to_node
        self.distance = from_node.distanceTo(to_node)
        self.isOneWay = isOneWay
        self.isBlocked = isBlocked
        
        if allowedVehicles is None:
            self.allowedVehicles = {"car", "motorbike", "walking"}
        else:
            self.allowedVehicles = set(allowedVehicles)
        
        self.travelTimes = {}
        if "car" in self.allowedVehicles:
            self.travelTimes["car"] = Car().travel_time(self.distance)
        if "motorbike" in self.allowedVehicles:
            self.travelTimes["motorbike"] = Motorbike().travel_time(self.distance)
        if "walking" in self.allowedVehicles:
            self.travelTimes["walking"] = Walking().travel_time(self.distance)

    def __str__(self):
        blocked_status = " (Đang bị chặn)" if self.isBlocked else ""
        oneway_status = " (Đường một chiều)" if self.isOneWay else ""
        allowed_vehicles = ", ".join(self.allowedVehicles)
        return (f"Đường đi từ {self.fromNode.Name} đến {self.toNode.Name}, "
                f"Khoảng cách: {self.distance:.2f} km, "
                f"Phương tiện được phép lưu thông: [{allowed_vehicles}]"
                f"{blocked_status}{oneway_status}\n")
    

    def __repr__(self):
        return f"Từ ({self.fromNode.Id} đi {self.toNode.Id}, {self.distance:.2f})"

    def canTraverse(self, vehicle_type):
        if self.isBlocked:
            return False
        return vehicle_type.lower() in self.allowedVehicles

    def getTravelTime(self, vehicle):
        return self.travelTimes.get(vehicle.lower(), float('inf'))

    def getWeight(self, vehicle_type, metric="distance"):
        if not self.canTraverse(vehicle_type):
            return float('inf')
        if metric == "distance":
            return self.distance
        elif metric == "time":
            return self.getTravelTime(vehicle_type)
        else:
            raise ValueError("Metric phải là 'distance' hoặc 'time'")