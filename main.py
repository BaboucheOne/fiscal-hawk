def main():
    import json
    from enum import Enum
    import os

    class Time(Enum):
        DAY = 'DAY'
        MONTH = 'MONTH'
        ANNUAL = 'ANNUAL'

    def to_monthly(value, time):
        if time == Time.DAY.value:
            return value * 30
        elif time == Time.MONTH.value:
            return value
        elif time == Time.ANNUAL.value:
            return value / 12
        else:
            return 0

    json_path = os.path.join(os.path.dirname(__file__), 'finances.json')
    with open(json_path, 'r') as f:
        data = json.load(f)

    total_income = 0
    print("Incomes per month:")
    for income in data.get('incomes', []):
        monthly = to_monthly(income['value'], income['time'])
        print(f"- {income['name']}: {monthly:.2f}")
        total_income += monthly

    total_expense = 0
    print("\nExpenses per month:")
    for expense in data.get('expenses', []):
        monthly = to_monthly(expense['value'], expense['time'])
        print(f"- {expense['name']}: {monthly:.2f}")
        total_expense += monthly

    print("\n--- Monthly Summary ---")
    print(f"Total income: {total_income:.2f}")
    print(f"Total expenses: {total_expense:.2f}")
    print(f"Net balance: {total_income - total_expense:.2f}")

if __name__ == "__main__":
    main()
