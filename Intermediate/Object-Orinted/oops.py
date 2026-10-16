# class Account:
#     def __init__(self, acc_no, acc_pass):
#         self.acc_no = acc_no
#         self.__acc_pass = acc_pass      # Private Class    (__ use to make for private atribute or method)

#     # public function
#     def reset_pass(self):
#         print(self.__acc_pass)


# acc1 = Account("DFBD89535", "AD09899")

# print(f"Account Number: {acc1.acc_no}")
# # print(f"Privat Password: {acc1.__acc_pass}")
# print(f"Public Password: {acc1.reset_pass()}")


class Person:
    __name = "Anonymous"

    def __hello(self):
        print("HELLO, Person.")

    def welcome(self):
        self.__hello()


p1 = Person()
# print(p1.__name)
# print(p1.__hello())
print(p1.welcome())
