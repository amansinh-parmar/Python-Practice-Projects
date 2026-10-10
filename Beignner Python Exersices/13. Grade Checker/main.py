print(" ------- GRADE CHECKER ------- ")

print('ENTER YOUR MARKS UPTO 100')

usr_input = float(input('ENTER MARKS: '))

if usr_input >= 90:
    print('CONGRATULATION, YOU GOT A+ GRADE.')
elif usr_input >= 80:
    print('VERY GOOD, YOU GOT A GRADE.')
elif usr_input >= 60:
    print('GOOD, YOU GOT B GRADE.')
elif usr_input >= 40:
    print('GOOD, YOU GOT C GRADE.')
else:
    print('YOU ARE FAIL..!!')
