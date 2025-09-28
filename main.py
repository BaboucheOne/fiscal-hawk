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
        print(f"- {income['name']}: {monthly:.2f}$")
        total_income += monthly

    total_expense = 0
    print("\nExpenses per month:")
    for expense in data.get('expenses', []):
        monthly = to_monthly(expense['value'], expense['time'])
        print(f"- {expense['name']}: {monthly:.2f}$")
        total_expense += monthly

    print("\n--- Monthly Summary ---")
    print(f"Total income: {total_income:.2f}$")
    print(f"Total expenses: {total_expense:.2f}$")
    net_balance = total_income - total_expense
    print(f"Net balance: {net_balance:.2f}$")

    saving = data.get('saving')
    if saving:
        saving_percent = saving.get('percentage', 0)
        saving_amount = net_balance * saving_percent / 100
        print(f"\nSaving ({saving_percent}% of net balance): {saving_amount:.2f}$")
        items = saving.get('items', [])
        total_item_percent = sum(item.get('percent', 0) for item in items)
        if total_item_percent != 100:
            print(f"WARNING: Saving items percent sum is {total_item_percent}%. You do not use all of your saving %.")
        print("Saving distribution:")
        for item in items:
            item_amount = saving_amount * item.get('percent', 0) / 100
            print(f"- {item['name']}: {item_amount:.2f}$ (target: {item['target']}$, {item['percent']}%)")
        net_balance_after_saving = net_balance - saving_amount
        print(f"\nNet balance after savings: {net_balance_after_saving:.2f}$")

if __name__ == "__main__":
    main()
