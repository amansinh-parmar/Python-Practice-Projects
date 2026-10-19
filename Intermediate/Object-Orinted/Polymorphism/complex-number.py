class Complex:
    def __init__(self, real, img):
        self.real = real
        self.img = img

    def showNumber(self):
        print(f"{self.real}i + {self.img}j")

    # Dunder Function
    def __add__(self, num2):
        newReal = self.real + num2.real
        newImg = self.img + num2.img
        return Complex(newReal, newImg)

    def __sub__(self, num2):
        newReal = self.real - num2.real
        newImg = self.img - num2.img
        return Complex(newReal, newImg)


num1 = Complex(2, 5)
num2 = Complex(4, 7)
print("Num1:")
num1.showNumber()
print("Num2:")
num2.showNumber()

num3 = num1 + num2
print("-----------")
print(f"Add Number: {num3.showNumber()}")

num3 = num2 - num1
print("\n-----------")
print(f"Subtraction: {num3.showNumber()}")
