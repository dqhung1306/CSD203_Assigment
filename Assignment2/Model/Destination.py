from math import atan2, degrees

def angle(x1, y1, x2, y2):
    angle = atan2(y2 - y1, x2 - x1)
    return degrees(angle) if angle >= 0 else degrees(angle) + 360

class Node:
    def __init__(self, Id, Name, x, y, Ltype= 'Khác'):
        self.Id = Id
        self.Name = Name
        self.x = x
        self.y = y
        self.locationType = Ltype 
        
    def __str__(self):
        return f"{self.Id}-{self.Name} ở ({self.x}, {self.y})"

    def __repr__(self):
        return f"Node({self.Id}, '{self.Name}', {self.x}, {self.y}, '{self.locationType}')"

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.Id == other.Id
        return False

    def __hash__(self):
        return hash(self.Id)

    def distanceTo(self, other):
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return float(f"{distance:.2f}")

    def navigate(self, prev, toNode):
        if prev is None:
            prev = self
        vx1 = self.x - prev.x
        vy1 = self.y - prev.y
        

        vx2 = toNode.x - self.x
        vy2 = toNode.y - self.y

        ang = angle(self.x, self.y, toNode.x, toNode.y) % 360
        cross = vx1 * vy2 - vy1 * vx2

        # Chỉ dẫn chi tiết
        if 45 < ang <= 135:
            return "Rẽ trái"
        elif 135 < ang <= 225:
            return "Đi thẳng"
        elif 225 < ang <= 315:
            return "Rẽ phải"
        elif ang > 315 or ang <= 45:
            if cross > 0:
                return "Quay đầu sang trái"
            elif cross < 0:
                return "Quay đầu sang phải"
            else:
                return "Quay đầu thẳng"
        else:
            return "Đi tiếp"


    def calculateAngle(self, toNode):
        return angle(self.x, self.y, toNode.x, toNode.y)