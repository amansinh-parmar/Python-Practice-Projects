FILE_NAME = "new_expense.txt"


# Add Expense
def add_expense():
    name = input("Enter Name: ").strip().upper()
    category = input("Enter Category: ").strip().upper()

    try:
        amount = float(input("Enter Amount: "))
        if amount < 0:
            print("Amount cannot be negative.")
            return
    except ValueError:
        print("Invalid amount, Please enter a number.")

    with open(FILE_NAME, "a") as file:
        file.write(f"{name} | {category} | {amount:.2f}\n")


# View Expense
def view_expense():
    try:
        with open(FILE_NAME, "r") as file:
            expense = file.readlines()

        if not expense:
            print("Expense not found.")
            return

        print("\n ============== VIEW ALL EXPENSES ============== ")
        print(f"{'Name':<20} {'Category':<15} {'Amount':>10}")
        print("-" * 47)

        for line in expense:
            parts = line.strip().split("|")

            if len(parts) == 3:
                name, category, amount = parts
                print(f"{name:<20} {category:<15} {float(amount):>10.2f}")

    except FileNotFoundError:
        print("Expense Not Found. Please Add an Expense First.")


# Search Expense
def search_expense():
    category_to_search = input("Enter category to search: ").strip().upper()

    found = False

    try:
        with open(FILE_NAME, "r") as file:
            print(f"\n ============ EXPENSE IN '{category_to_search}' ============ ")

            for line in file:
                parts = line.strip().split("|")

                if len(parts) == 3:
                    name, category, amount = parts

                    if category.strip().upper() == category_to_search:
                        print(
                            f"Name: {name:<12}"
                            f"Category: {category:<12}"
                            f"Amount: {float(amount):>8.2f}"
                        )
                        found = True

        if not found:
            print("No Expenses found in this category.")

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

            print(f"Total Spending: {total:.2f}")

    except FileNotFoundError:
        print("Expense Not Found!!")
        print(f"Total Spending: {total:.2f}")


# USER INPUT
def main():
    while True:
        print("\n ============ EXPENSE TRACKER ============ ")
        print("1. Add Expense")
        print("2. View All Expense")
        print("3. Search Expense Category")
        print("4. Calclate Total Expenses")
        print("5. Exit")

        choice = input("Enter Choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expense()
        elif choice == "3":
            search_expense()
        elif choice == "4":
            calculate_total()
        elif choice == "5":
            print("GOODBYEE!!!!")
            break
        else:
            print("Invalid choice. Try Again.")


__name__ == "__main__"
main()
