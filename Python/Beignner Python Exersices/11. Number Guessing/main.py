import random

number = random.randint(1, 10)
attempt = 0

print('THIS IS A NUMBER GUESSING GAME')
print("I'M THINKING A NUMBER BETWEEN 1 TO 10")

while True:
    usr_guess = int(input('ENTER YOUR GUESS: '))
    attempt += 1
    
    if usr_guess < number:
        print('Your number is LOWER than the guessing. Please Try Again')
    elif usr_guess > number:
        print('Your number is HIGHER than the guessing. Please Try Again')
    else:
        print('CORRECT, You are guess a RIGHT NUMBER.')
        break

