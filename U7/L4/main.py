from rectangle import Rectangle
from random import randint

rectangles = []
for i in range(100):
    rectangles.append(Rectangle(randint(30, 50), randint(5, 25)))
    print(f"Rectangle {i} -----------------")
    rectangles[i].area()
    rectangles[i].perimeter()