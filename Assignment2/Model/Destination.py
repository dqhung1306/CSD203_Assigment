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
        if prev is None or prev == self:
            return "Bắt đầu hành trình"
        #vt1
        vx1 = self.x - prev.x
        vy1 = self.y - prev.y
        #vt2
        vx2 = toNode.x - self.x
        vy2 = toNode.y - self.y

        ang = angle(self.x, self.y, toNode.x, toNode.y)
        prev_ang = angle(prev.x, prev.y, self.x, self.y)
        relative_angle = (ang - prev_ang) % 360

        if relative_angle < 10 or relative_angle > 350:
            return "Đi thẳng"
        elif 10 <= relative_angle < 45:
            return f"Rẽ phải nhẹ khoảng {int(relative_angle)} độ"
        elif 45 <= relative_angle <= 135:
            return f"Rẽ phải khoảng {int(relative_angle)} độ"
        elif 135 < relative_angle < 170:
            return f"Rẽ trái nhẹ khoảng {int(360 - relative_angle)} độ"
        elif 170 <= relative_angle <= 190:
            return "Quay đầu"
        elif 190 < relative_angle <= 225:
            return f"Rẽ trái khoảng {int(360 - relative_angle)} độ"
        elif 225 < relative_angle <= 350:
            return f"Rẽ trái nhẹ khoảng {int(360 - relative_angle)} độ"
        else:
            return f"Rẽ phải khoảng {int(relative_angle)} độ"


    def calculateAngle(self, toNode):
        return angle(self.x, self.y, toNode.x, toNode.y)