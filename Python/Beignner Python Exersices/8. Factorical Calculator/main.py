# Calculate the factorial of a given number
# Example: 4 factocial = 4*3*2*1. Factorial of 1 & 0 = 1
# 7 = 7*6*5*4*3*2*1

# USE:
# 1. User input
# 2. Function
# 3. f-string

def factorial_calculator(number):
    result = 1 
    for i in range(1, number + 1):
        result *= i
    return result

usr_num = int(input("Enter any number that count into Factorial: "))
print(f'Your {usr_num} Factorial number is {factorial_calculator(usr_num)}')