
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, DataTable, Static
from textual.containers import Container, Horizontal
import json
import os
from enum import Enum

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

class FinanceApp(App):
    BINDINGS = [("q", "quit", "Quit")]
    TITLE = "Finances Summary"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Horizontal(
                Tree("Incomes", id="incomes_tree"),
                Tree("Expenses", id="expenses_tree"),
                Tree("Saving", id="saving_tree"),
            ),
            Static("\n"),
            DataTable(id="summary_table"),
        )
        yield Footer()

    def on_mount(self):
        self.title = self.TITLE

        json_path = os.path.join(os.path.dirname(__file__), 'finances.json')
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Incomes tree
        incomes_tree = self.query_one("#incomes_tree", Tree)
        total_income = 0
        for income in data.get('incomes', []):
            monthly = to_monthly(income['value'], income['time'])
            incomes_tree.root.add_leaf(f"{income['name']}: {monthly:.2f}$ ({income['time']})")
            total_income += monthly
        incomes_tree.root.expand()

        # Expenses tree
        expenses_tree = self.query_one("#expenses_tree", Tree)
        total_expense = 0
        for expense in data.get('expenses', []):
            monthly = to_monthly(expense['value'], expense['time'])
            expenses_tree.root.add_leaf(f"{expense['name']}: {monthly:.2f}$ ({expense['time']})")
            total_expense += monthly
        expenses_tree.root.expand()

        # Saving tree
        saving_tree = self.query_one("#saving_tree", Tree)
        saving = data.get('saving')
        monthly_saving_total = 0
        if saving:
            warning_percentage = saving.get('warning_percentage', 0)
            items = saving.get('items', [])
            for item in items:
                monthly_cost = item['target'] / 12
                saving_tree.root.add_leaf(f"{item['name']}: {monthly_cost:.2f}$ (target: {item['target']}$)")
                monthly_saving_total += monthly_cost
            saving_tree.root.expand()

        net_balance = total_income - total_expense
        annual_net_balance = net_balance * 12
        net_balance_after_saving = net_balance - monthly_saving_total

        # Summary table
        table = self.query_one("#summary_table", DataTable)
        table.add_columns("Item", "Monthly ($)", "Annual ($)")
        table.add_rows([
            ["Total income", f"{total_income:.2f}", f"{total_income*12:.2f}"],
            ["Total expenses", f"{total_expense:.2f}", f"{total_expense*12:.2f}"],
            ["Net balance", f"{net_balance:.2f}", f"{annual_net_balance:.2f}"],
            ["Saving cost", f"{monthly_saving_total:.2f}", f"{monthly_saving_total*12:.2f}"],
            ["Net after saving", f"{net_balance_after_saving:.2f}", f"{net_balance_after_saving*12:.2f}"],
        ])
        table.cursor_type = "row"
        table.focus()

def main():
    FinanceApp().run()

if __name__ == "__main__":
    main()
