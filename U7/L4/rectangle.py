class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def area(self):
        print(f"Area = {self.length * self.width}")
    
    def perimeter(self):
        print(f"Perimeter = {2 * (self.length + self.width)}")
    
    def double_dimensions(self):
        self.length *= 2
        self.width *= 2

    def half_dimensions(self):
        self.length /= 2
        self.width /= 2