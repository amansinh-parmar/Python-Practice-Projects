# Parent Class
class Car:
    color = "Black"

    @staticmethod
    def start():
        return "Car Started...."

    @staticmethod
    def stopped():
        return "Car Not Working..!!"


# Child Class
# Single Inheritance
class BMW(Car):
    def __init__(self, brand):
        self.brand = brand


# Multi Level Inheritance
class M4(BMW):
    def __init__(self, brand, type):
        super().__init__(brand)
        self.type = type


class A7(BMW):
    def __init__(self, brand, type):
        super().__init__(brand)
        self.type = type


bmw = M4("BMW M4", "Petrol")
audi = A7("Audi A7", "Electric")

print(f"Car: {bmw.brand}")
print(f"Type: {bmw.type}")
print(f"Color: {bmw.color}")
print(f"{bmw.start()}\n")
print(f"Car: {audi.brand}")
print(f"Type: {audi.type}")
print(f"{bmw.stopped()}\n")


# Multiple Inheritance
class A:
    varA = "Welcome to CLass A"


class B:
    varB = "Welcome to CLass B"


class C(A, B):
    varC = "Welcome to CLass C"


c1 = C()

print(c1.varC)
print(c1.varB)
print(c1.varA)
