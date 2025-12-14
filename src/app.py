from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, DataTable, Static
from textual.containers import Container, Horizontal

from src.controller.account_controller import AccountController
from src.controller.simulation_controller import SimulationController
from src.screen.compound_interest_screen import CompoundInterestScreen
from src.screen.compound_interest_simulation_screen import (
    CompoundInterestSimulationScreen,
)
from src.service_locator import ServiceLocator
from src.utility import yearly_adjusted_monthly_value, to_monthly


class FinanceApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "compound", "Show Compound Interest"),
        ("s", "simulation", "Show Compound Interest Simulation"),
    ]
    TITLE = "Finances Summary"

    def __init__(self, **kwargs):
        super(FinanceApp, self).__init__(**kwargs)
        self.__account_controller: AccountController = ServiceLocator.get_dependency(AccountController)
        self.__simulation_controller: SimulationController = ServiceLocator.get_dependency(SimulationController)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Horizontal(
                Tree("Incomes", id="incomes_tree"),
                Tree("Planned Expenses", id="planned_expenses_tree"),
                Tree("Expenses", id="expenses_tree"),
                Tree("Saving", id="saving_tree"),
            ),
            Static("\n"),
            DataTable(id="summary_table"),
        )
        yield Footer()

    def on_mount(self):
        self.title = self.TITLE
        self.load_finances()

    def load_finances(self):
        # Incomes tree
        incomes_tree = self.query_one("#incomes_tree", Tree)
        total_income = 0
        for income in self.__account_controller.incomes:
            income_value = yearly_adjusted_monthly_value(income)
            monthly = to_monthly(income_value, income.time)
            incomes_tree.root.add_leaf(
                f"{income.name}: {monthly:.2f}$ (weighted annual average)"
            )
            total_income += monthly
        incomes_tree.root.expand()

        # Expenses tree
        planned_expenses_tree = self.query_one("#planned_expenses_tree", Tree)
        planned_total_expense = 0
        for expense in self.__account_controller.planned_expenses:
            monthly = to_monthly(expense.value, expense.time)
            planned_expenses_tree.root.add_leaf(
                f"{expense.name}: {monthly:.2f}$ ({expense.time})"
            )
            planned_total_expense += monthly
        planned_expenses_tree.root.expand()

        # Saving tree
        saving_tree = self.query_one("#saving_tree", Tree)
        monthly_saving_total = 0
        for saving in self.__account_controller.saving_configuration.savings:
            monthly_cost = saving.target / 12
            saving_tree.root.add_leaf(
                f"{saving.name}: {monthly_cost:.2f}$ (target: {saving.target}$)"
            )
            monthly_saving_total += monthly_cost
        saving_tree.root.expand()

        # Expenses tree
        expenses_tree = self.query_one("#expenses_tree", Tree)
        saving_names = {saving.name.lower(): saving.target for saving in self.__account_controller.saving_configuration.savings}
        for expense in sorted(self.__account_controller.expenses, key=lambda e: e.date):
            leaf_text: str = f"{expense.name}: {expense.value:.2f}$"

            if expense.link.lower() in saving_names:
                saving_target: float = saving_names[expense.link.lower()]
                link_percentage: float = 0.0
                if saving_target > 0:
                    link_percentage: float = expense.value / saving_names[expense.link.lower()] * 100.0
                leaf_text += f" ({link_percentage:.2f}% of {expense.link.upper()})"

            expenses_tree.root.add_leaf(leaf_text)
        expenses_tree.root.expand()

        net_balance = total_income - planned_total_expense
        annual_net_balance = net_balance * 12
        net_balance_after_saving = net_balance - monthly_saving_total

        table = self.query_one("#summary_table", DataTable)
        table.add_columns("Item", "Monthly ($)", "Annual ($)")
        table.add_rows(
            [
                ["Total income", f"{total_income:.2f}", f"{total_income*12:.2f}"],
                ["Total planned expenses", f"{planned_total_expense:.2f}", f"{planned_total_expense*12:.2f}"],
                ["Net balance", f"{net_balance:.2f}", f"{annual_net_balance:.2f}"],
                [
                    "Saving cost",
                    f"{monthly_saving_total:.2f}",
                    f"{monthly_saving_total*12:.2f}",
                ],
                [
                    "Net after saving",
                    f"{net_balance_after_saving:.2f}",
                    f"{net_balance_after_saving*12:.2f}",
                ],
            ]
        )
        table.cursor_type = "row"
        table.focus()

    def action_compound(self):
        self.push_screen(
            CompoundInterestScreen(
            )
        )

    def action_simulation(self):
        self.push_screen(
            CompoundInterestSimulationScreen(
            )
        )
