print (' ------- EXPENSE CALCULATOR -------')

income = float(input('Enter your income: '))

rent = float(input('Enter Rent: '))
food = float(input('Enter Food: '))
transport = float(input('Enter Transportation: '))
shopping = float(input('Enter Shopping: '))
other = float(input('Enter Other Expense: '))

expense = rent + food + transport + shopping + other
remaining = income - expense

print('\n ----- Expense Summary -----')
print(f'Income: {income}')
print(f'Total Expenses: AED{expense}')
print(f'Money Remaining: AED{remaining}')

if remaining > 0:
    print('You are Within your Budget.')
elif remaining == 0:
    print('You spent your Entire Income.')
else:
    print('You have Exceeded your Budget')