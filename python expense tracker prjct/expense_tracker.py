import json
import os

DATA_FILE = "expenses.json"

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(expenses):
    try:
        amount = float(input("Enter expense amount: "))
        category = input("Enter category (Food, Transport, Entertainment, etc.): ").strip()
        description = input("Enter description: ").strip()
        expense = {
            "amount": amount,
            "category": category,
            "description": description
        }
        expenses.append(expense)
        save_expenses(expenses)
        print("Expense added successfully.\n")
    except ValueError:
        print("Invalid amount entered. Please try again.\n")

def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded.\n")
        return
    print("\n--- All Expenses ---")
    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. {exp['category']} - ${exp['amount']:.2f} : {exp['description']}")
    print()

def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        idx = int(input("Enter the number of the expense to delete: "))
        if 1 <= idx <= len(expenses):
            removed = expenses.pop(idx - 1)
            save_expenses(expenses)
            print(f"Removed expense: {removed['category']} - ${removed['amount']:.2f}\n")
        else:
            print("Invalid number.\n")
    except ValueError:
        print("Invalid input.\n")

def summary_by_category(expenses):
    if not expenses:
        print("No expenses recorded.\n")
        return
    summary = {}
    for exp in expenses:
        summary[exp['category']] = summary.get(exp['category'], 0) + exp['amount']
    print("\n--- Expense Summary by Category ---")
    for category, total in summary.items():
        print(f"{category}: ${total:.2f}")
    print()

def main():
    expenses = load_expenses()
    while True:
        print("Expense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Expense Summary")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            summary_by_category(expenses)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")

if __name__ == "__main__":
    main()
