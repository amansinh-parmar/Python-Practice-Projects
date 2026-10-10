FILE_NAME = "expenses.txt"


def add_expense():
    name = input("Enter expense name: ").strip().upper()
    category = input("Enter category: ").strip().upper()
    
    try:
        amount = float(input("Enter amount: "))
        if amount < 0:
            print("Amount cannot be negative.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    # Open file in append mode and write the expense
    with open(FILE_NAME, "a") as file:
        file.write(f"{name}|{category}|{amount:.2f}\n")

    print("Expense added successfully!")


def view_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            expenses = file.readlines()

        if not expenses:
            print("No expenses found.")
            return

        print("\n===== ALL EXPENSES =====")
        print(f"{'Name':<20} {'Category':<15} {'Amount':>10}")
        print("-" * 47)

        for line in expenses:
            parts = line.strip().split("|")

            if len(parts) == 3:
                name, category, amount = parts
                print(f"{name:<20} {category:<15} {float(amount):>10.2f}")

    except FileNotFoundError:
        print("No expenses found. Add an expense first.")


def search_expenses():
    category_to_search = input(
        "Enter category to search: "
    ).strip().upper()

    found = False

    try:
        with open(FILE_NAME, "r") as file:
            print(f"\n===== EXPENSES IN '{category_to_search}' =====")

            for line in file:
                parts = line.strip().split("|")

                if len(parts) == 3:
                    name, category, amount = parts

                    if category.strip().lower() == category_to_search:
                        print(
                            f"Name: {name} | "
                            f"Category: {category} | "
                            f"Amount: {float(amount):.2f}"
                        )
                        found = True

        if not found:
            print("No expenses found in this category.")

    except FileNotFoundError:
        print("No expenses found. Add an expense first.")


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

        print(f"Total spending: {total:.2f}")

    except FileNotFoundError:
        print("No expenses found.")
        print(f"Total spending: {total:.2f}")


def main():
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Search expenses")
        print("4. Calculate total spending")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            search_expenses()
        elif choice == "4":
            calculate_total()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()