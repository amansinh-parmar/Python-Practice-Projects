# Check if a user input number is prime
# Prime number is only divisible by 1 and itself
# 1 is not a prime number

# USE
# 1. User Input
# 2. Functions
# 3. f-strings

# Additional Tasks -> Optimize the Program

# use function to check prime number
def is_prime(number):
    if number < 2:
        return False

    for i in range(2, number):
        if number % i == 0:
            return False

    return True

# Check user number is Prime or Not with if-else
usr_input = input('Enter the number here: ')
number = int(usr_input)

if is_prime(number):
    print(f'{number} is Prime')
else:
    print(f'{number} is Not Prime')