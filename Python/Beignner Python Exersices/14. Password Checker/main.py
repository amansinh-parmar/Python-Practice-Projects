print(' ------- PASSWORD CHECKER ------- \n')

password = input('Enter your PASSWORD: ')

score = 0
advice = []

# Check Length
if len(password) >= 8:
    score += 1
else:
    advice.append('Use at least 8 characters.')

# Check Uppercase
if any(char.isupper() for char in password):
    score += 1
else: 
    advice.append('Use any Uppercase Character (A-Z).')

# Check Lowercase
if any(char.islower() for char in password):
    score += 1
else:
    advice.append('Use Lowercase Character (a-z).')

# Check Number
if any(char.isdigit() for char in password):
    score += 1
else:
    advice.append('Use any Number (0-9)')

# Check Special Character
if any(not char.isalnum() for char in password):
    score += 1
else:
    advice.append('Use any Special Chacter (!, @, #, $, etc)')


# Display Result 
print(f'\n* Password Score is {score}/5')

if score == 5:
    print('- Strong Password')
elif score >= 3:
    print("- Medium Password\n")
    print('Advice')
    for tip in advice:
        print('-', tip)
else:
    print('- Weak Password\n')
    print('Advice')
    for tip in advice:
        print('-', tip)
