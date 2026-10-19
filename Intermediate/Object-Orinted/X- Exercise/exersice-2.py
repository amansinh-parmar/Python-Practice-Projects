class Employee:
    def __init__(self, role, dept, salary):
        self.role = role
        self.dept = dept
        self.salary = salary

    def showDetails(self):
        print(f"Employee Role: {self.role}")
        print(f"  ''     Depatartment: {self.dept}")
        print(f"  ''     Salary: {self.salary}")


class Engineer(Employee):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        super().__init__("Engineer", "IT", "75,000")


# e1 = Employee("Accountant", "Finance", "60,000")
# e1.showDetails()

eng1 = Engineer("Elon Musk", 40)
eng1.showDetails()
