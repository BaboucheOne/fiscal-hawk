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
    print(f"Net balance (monthly): {net_balance:.2f}$")

    # Annual net balance for savings
    annual_net_balance = net_balance * 12
    print(f"Net balance (annual): {annual_net_balance:.2f}$")

    saving = data.get('saving')
    if saving:
        warning_percentage = saving.get('warning_percentage', 0)
        items = saving.get('items', [])
        print("\nSaving items:")
        for item in items:
            monthly_cost = item['target'] / 12
            print(f"- {item['name']} (target: {item['target']}$, monthly: {monthly_cost:.2f}$)")

        # Check if all targets are possible (annual)
        possible_targets = [item['target'] for item in items if item.get('target', 0) <= annual_net_balance]
        impossible_targets = [item for item in items if item.get('target', 0) > annual_net_balance]
        total_targets = sum(item.get('target', 0) for item in items)
        warning_amount = annual_net_balance * warning_percentage / 100

        if len(impossible_targets) > 0:
            print("WARNING: The following saving targets are not possible with your annual net balance:")
            for item in impossible_targets:
                print(f"- {item['name']} (target: {item['target']}$)")
        elif total_targets > warning_amount:
            print(f"WARNING: The total saving targets ({total_targets}$) exceed your warning percentage ({warning_percentage}% = {warning_amount:.2f}$) of your annual net balance.")
    # Show total monthly saving cost
    monthly_saving_total = sum(item['target'] / 12 for item in items)
    print(f"\nTotal saving cost per month: {monthly_saving_total:.2f}$")
    net_balance_after_saving = net_balance - monthly_saving_total
    print(f"Net balance after savings (monthly): {net_balance_after_saving:.2f}$")

if __name__ == "__main__":
    main()
