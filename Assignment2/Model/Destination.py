from math import atan2, degrees
def angle(x1, y1, x2, y2):
    angle = atan2(y2 - y1, x2 - x1)
    return degrees(angle) if angle >= 0 else degrees(angle) + 360
class Node:
    def __init__(self, Id, Name, x, y):
        self.Id = Id
        self.Name = Name
        self.x = x
        self.y = y
        
    def __str__(self):
        return f"{self.Name}, ({self.x}, {self.y})"

    def distanceTo(self, other):
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return float(f"{distance:.2f}")

    def navigate(self, toNode):
        angle = self.calculate_angle(toNode)
        if angle > 45 and angle < 135:
            return "Rẽ trái"
        elif angle > 135 and angle < 225:
            return "Đi thẳng"
        elif angle > 225 and angle < 315:
            return "Rẽ phải"
        else:
            return "Quay đầu"

    def calculate_angle(self, toNode):
        return angle(self.x, self.y, toNode.x, toNode.y)