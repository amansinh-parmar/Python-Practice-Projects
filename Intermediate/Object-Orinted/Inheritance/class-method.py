class Person:
    name = "Anonymous"

    # def changeName(self, name):
    #     # Person.name = name
    #     self.__class__.name = 'Apex'

    @classmethod
    def changeName(cls, name):
        cls.name = name


p1 = Person()
print(f"Person Name: {p1.name}\n")

p1.changeName("Jack Reacher")
print(f"Person Change Name: {p1.name}\n")
