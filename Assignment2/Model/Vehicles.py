class Vehicle:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed  # km/h

    def travel_time(self, distance):
        return (distance / self.speed) * 60  # phút
    
    def __str__(self):
        return f"{self.name} (Speed: {self.speed} km/h)"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', {self.speed})"

class Car(Vehicle):
    def __init__(self):
        super().__init__('Car', 60)

class Motorbike(Vehicle):
    def __init__(self):
        super().__init__('Motorbike', 80) 

class Walking(Vehicle):
    def __init__(self):
        super().__init__('Walking', 7)