class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return (22/7) * self.radius**2

    def parimeter(self):
        return 2 * (22/7) * self.radius


c1 = Circle(21)
print(f"Circle Area: {c1.area()}")
print(f"Circle Perimeter: {c1.parimeter()}")
