print('----- CALCULATOR -----')

num1 = float(input('ENTER YOUR FIRST NUMBER: '))
oprator = input("CHOOSE THE OPRATOR ('+', '-', 'x', '/'): ")
num2 = float(input('ENTER YOUR SECOND NUMBER: '))

if oprator == '+':
    result = num1 + num2
elif oprator == '-':
    result = num1 - num2
elif oprator == 'x':
    result = num1 * num2
elif oprator == '/':
    if num2 != 0:
        result = num1 / num2
    else:
        print('CAN NOT DIVIDE BY ZERO.')
else:
    print('INVALID OPRATOR..!!')

print(f'RESULT: {result}')