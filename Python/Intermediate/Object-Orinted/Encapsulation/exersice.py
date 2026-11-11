# ====>> STUDENT NAME AND MARKS AND FIND AVARAGE MARKS <<====
# class Student:
#     def __init__(self, name, marks):
#         self.name = name
#         self.marks = marks

#     def get_avg(self):
#         sum = 0
#         for val in self.marks:
#             sum += val
#         print(f"-->> Hi {self.name}, Your avarage marks is {sum/4}")


# studnet = Student("Jack", [90, 97, 98, 95])
# print(f"Student name is {studnet.name} and His Marks is {studnet.marks}.")
# studnet.get_avg()

# studnet.name = "Apex"
# print(f"Student name is {studnet.name} and His Marks is {studnet.marks}.")
# studnet.get_avg()


# ====>> ACCOUNT BALANCE SHEET <<====
class Account:
    # Use Object Attributes
    def __init__(self, balance):
        self.balance = balance

    # Use Methods
    @staticmethod
    def total_balance():
        print("\nENTER CREDIT ENTRY:")
        credit = int(input())
        print("\nENTER DEBIT ENTRY:")
        debit = int(input())
        total = credit - debit
        return total


# get total in variable
balances_sheet = Account.total_balance()
account = Account(balances_sheet)

print("\n========== ACCOUNT DETAILS ==========")
print("Account No.\nWAZX8234897")

print(f"\nBalance\n{account.balance:,}")