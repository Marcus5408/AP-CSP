from rectangle import Rectangle
from random import randint

def run_iteration(amt: int):
    rectangles = []
    for i in range(10000):
        rectangles.append(Rectangle(
            length=randint(30, 50), 
            width=randint(5, 25),
            position=(randint(0, 50), randint(0, 50))
            ))

    main_rectangle = Rectangle(10, 15, (20, 10))

    # determine if any rectangles overlap with main_rectangle. position is top-left corner
    collisions = 0
    for rect in rectangles:
        if (rect.position[0] < main_rectangle.position[0] + main_rectangle.length and
            rect.position[0] + rect.length > main_rectangle.position[0] and
            rect.position[1] < main_rectangle.position[1] + main_rectangle.width and
            rect.position[1] + rect.width > main_rectangle.position[1]):
            collisions += 1
    print(f"Number of collisions: {collisions}")
    print(f"% Collisions: {(collisions / 10000) * 100}%")

for _ in range(1000):
    run_iteration(10000)