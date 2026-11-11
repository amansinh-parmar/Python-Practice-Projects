#Take user input and print if the number is ODD or EVEN.
user = int(input('Enter any number and check whether this is ODD or EVEN Number: '))

if user % 2 == 0:
    print(f"This {user} number is a EVEN NUMBER")
else:
    print(f"This {user} number is a ODD NUMBER")
