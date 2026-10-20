FILE_NAME = "Python-Practice-Projects/Beignner Python Exersices/15. Expense Calculator/expense.txt"


# Add Expenses
def add_expense():
    name = input("Enter Expense Name: ").strip().upper()
    category = input("Enter the Category: ").strip().upper()

    try:
        amount = float(input("Enter Amount: "))
        if amount <= 0:
            print("The Amount cannot be valid in Negative.")
            return
    except ValueError:
        print("Invalid amount. Please enter a valid nnumber.")

    try:
        with open(FILE_NAME, "a") as file:
            file.write(f"{name} | {category} | {round(amount, 2)}\n")
        print("Expense added successfully.")

    except OSError as error:
        print(f"Error saving expense: {error}")


# View Expenses
def view_expense():
    try:
        with open(FILE_NAME, "r") as file:
            expense = file.readlines()

        if not expense:
            print("Expense not found.")
            return

        print("\n=============== VIEW ALL EXPENSES ===============")
        print(f"{'Name':<20} {'Category':<15} {'Amount':>10}")
        print("-" * 47)

        for line in expense:
            parts = line.strip().split("|")

            if len(parts) == 3:
                name, category, amount = parts

                try:
                    print(
                        f"{name.strip():<20} {category.strip():<15} {float(amount.strip()):>10.2f}"
                    )
                except ValueError:
                    print(f"Skipping Invalid Record: {line.strip()}")

    except FileNotFoundError:
        print("Expense not found. Please add an Expense First.")


# Search Expense
def search_expense():
    category_search = input("Enter Category to Search Expense: ").strip().upper()

    found = False

    try:
        with open(FILE_NAME, "r") as file:
            print(f"\n============= EXPENSES IN {category_search} =============")

            for line in file:
                parts = line.strip().split("|")

                if len(parts) == 3:
                    name, category, amount = parts

                    if category.strip().upper() == category_search:
                        print(
                            f"Name: {name:<12}"
                            f"Category: {category:<12}"
                            f"Amounut: {float(amount):>5.2f}"
                        )
                        found = True

            if not found:
                print("No Expenses found in this Category.")

    except FileNotFoundError:
        print("No Expense Found. Add Your Expense First.")


# Calculate Expense
def calculate_total():
    total = 0.0

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                parts = line.strip().split("|")

                if len(parts) == 3:
                    try:
                        amount = float(parts[2])
                        total += amount
                    except ValueError:
                        continue

            print(f"Total Spending: AED {total:.2f}")

    except FileNotFoundError:
        print("Expense not found.")
        print(f"Total Spending: AED {total:.2f}")


# USER INPUT
def main():
    while True:
        print("\n============== Expense Tracker ============== ")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expenses Category")
        print("4. Calculate Total Expenses")
        print("5. Exit")

        choice = int(input("Enter Choice: "))

        if choice == 1:
            add_expense()
        elif choice == 2:
            view_expense()
        elif choice == 3:
            search_expense()
        elif choice == 4:
            calculate_total()
        elif choice == 5:
            print("GOOD BYE..!!")
            break
        else:
            print("Invalid Choice. Try Again.")


__name__ == "__main__"
main()
