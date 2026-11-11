class NewLife:
    # default constructor
    def __init__(self):
        pass

    # decorator
    @staticmethod
    def greeting():
        print("Please enter your name:")
        user = input().upper()
        print("\n-----------------------------------")
        print(f"\nHello, {user}")
        return user

    # parameterized constructor
    def __init__(self, health, work, investment):
        self.health = health.upper()
        self.earning = work.upper()
        self.investment = investment.upper()
        print("CREATE A NEW LIFE")


name = NewLife.greeting()

print("\n============ LAST THREE MONTHS ============ ")
three_month = NewLife("Exersice", "Python", "Strategy")

print(f"PERSONAL HEALTH: '{three_month.health}'")
print(f"COMLPETE UNDERSTANDING: '{three_month.earning}'")
print(f"DISCIPLE AND CONSISTENCY: '{three_month.investment}'\n")

print("\n============ NEW YEAR ============ ")
next_year = NewLife("Meditation", "Machine Learning", "new skils")

print(f"MENTAL HEALTH: '{next_year.health}'")
print(f"GET JOB: '{next_year.earning}'")
print(f"HUSTLE: '{next_year.investment}'")
