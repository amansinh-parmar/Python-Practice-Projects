class Student:
    def __init__(self, phy, chem, math):
        self.phy = phy
        self.chem = chem
        self.math = math

    # def calcPercentage(self):
    #     self.percentage = (self.phy + self.chem + self.math) / 3  # percentage

    @property
    def percentage(self):
        return (self.phy + self.chem + self.math) / 3


student = Student(98, 95, 97)
print(f"Student Percentage: {round (student.percentage, 2)}%\n")

student.phy = 86
print(f"Change Physics Marks and Student Percentage: {round(student.percentage, 2)}%")
