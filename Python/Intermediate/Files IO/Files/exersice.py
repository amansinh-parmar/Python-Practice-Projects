file_name = 'expense.txt'

def add_expense():
    name = input('Enter Expense Name: ').strip()
    category = input('Enter Category: ').strip()

    # TODO
    try:
        amount = float(input('Enter Amount: '))
        if amount < 0:
            print("Amount cannot not be Nagative.")
    except ValueError:
        print('Invalid amount. Please enter a number.')
        return
    
    with open(file_name, 'a') as f:
        f.write(f'{name} | {category} | {amount:.2f}\n')

    print('Expense Amount Added Successfully.')

def view_expense():
    try:
        with open(file_name, 'r') as f:
            expense = f.readline()

        if not expense:
            print('No Expenese Found.')
            return

        print(' ======= All Expense ======= ')
        print(f'{'Name':<20}, {'Category':<15}, {'Amount':>10}')
        print("-", * 47)

        for line in expense:
            parts = line.strip().strip("|")

            if len(parts) == 3:
                name, category, amount = parts
                print(f"{name:<20} {category:<15} {float(amount):<10.2f}")

    except FileNotFoundError:
        print('No Expense Found. Please Add on Expense First.')

def search_expense():
    category_to_search = input('Enter Category to Search: ').strip().lower()

    found = False

    try:
        with open(file_name, 'r') as f:
            print(f'\n ======= Expenese in {category_to_search} ======= ')

            for line in f:
                parts = line.strip().split()

                if len(parts) == 3:
                    name, category, amount = parts

                    if category.strip().lower() == category_to_search:
                        print(
                            f'Name: {name} | '
                            f'Category: {category} | '
                            f'Amount: {float(amount):.2f}'
                        )

                        found = True

        if not found:
            print("No Expenses Found in This Category.")

    except FileNotFoundError:
        print('No Expense Found, Add an Expense First.')

def calculate_total():
    total = 0.0

    try:
        with open(file_name, 'r') as f:
            for line in f:
                parts = line.strip().split('|')

                if len(parts) == 3:
                    try:
                        amount = float(parts[2])
                        total += amount
                    except ValueError:
                        continue
        print(f'Total Spending: {total:.2f}')

    except FileNotFoundError:
        print("No Expense File Found.")
        print(f'Total Spending: {total:.2f}')


def main():
    while True:
        print("\n ======== EXPENSE TRACKER ======== ")
        print('1. Add Expense')
        print('2. View All Expenses')
        print('3. Search Expense')
        print('4. Calculate Total Spending')
        print('5. Exit')

        choice = int(input('Choose an Option: ').strip())

        if choice == 1:
            add_expense()
        elif choice == 2:
            view_expense()
        elif choice == 3:
            search_expense()
        elif choice == 4:
            calculate_total()
        elif choice == 5:
            print('GOODBYE!!')
        else:
            print('Invalid Choice, Please Try Again.')

if __name__ == '__main__':
    main()