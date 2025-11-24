import random
import statistics
from typing import List, Dict

import plotext as plt
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, DataTable, Static
from textual.containers import Container, Horizontal
from textual.screen import Screen
import yaml
import os
from enum import Enum

from textual_plotext import PlotextPlot


# ------------------ Finance Helpers ------------------

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

def yearly_adjusted_monthly_value(entry):
    base_value = entry["value"]
    time = entry["time"]
    monthly_base = to_monthly(base_value, time)

    future_value = entry.get("future_value")
    future_date = entry.get("future_date")

    if not future_value or not future_date:
        return monthly_base

    year, month = map(int, future_date.split("-"))

    new_months = max(0, 12 - (month - 1))
    old_months = 12 - new_months

    monthly_future = to_monthly(future_value, time)

    annual_total = old_months * monthly_base + new_months * monthly_future
    monthly_average = annual_total / 12

    return monthly_average

def compound_interest_calculator(
        current_value: float,
        monthly_contribution: float,
        annual_rate: float,
        years: float,
        compounds_per_year: int = 12
) -> float:
    r = annual_rate
    n = compounds_per_year
    t = years
    p = current_value
    pmt = monthly_contribution

    future_p = p * (1 + r / n) ** (n * t)

    if pmt > 0:
        future_pmt = pmt * ((1 + r / n) ** (n * t) - 1) / (r / n)
    else:
        future_pmt = 0

    return future_p + future_pmt



def monte_carlo_path(start_value, monthly_contribution, years, min_rate, max_rate):
    value = start_value
    results = [value]

    for _ in range(years):
        r = random.uniform(min_rate, max_rate)

        for _ in range(12):
            value = value * (1 + r / 12) + monthly_contribution

        results.append(value)

    return results


# ------------------ Compound Interest Screen ------------------

class CompoundInterestScreen(Screen):
    BINDINGS = [("b", "back", "Back")]

    def __init__(self, market_data, simulation_data, saving_items: List[Dict]):
        super().__init__()
        self.market_data = market_data
        self.simulation_data = simulation_data
        self.saving_items = saving_items

    def compose(self) -> ComposeResult:
        yield Header()
        yield PlotextPlot(id="chart_area")
        yield Footer()

    def on_mount(self):
        self.draw_chart()

    def draw_chart(self):
        chart = self.query_one("#chart_area", PlotextPlot).plt

        etfs = self.market_data.get('etf', [])

        start_year = 2025
        until_year = self.simulation_data.get('until_year', 2050)
        annual_rate = self.simulation_data.get('annual_rate', 0.1)
        years_list = list(range(start_year, until_year + 1))

        chart.clear_figure()

        for etf in etfs:
            start_value = etf['price']
            etf_name = etf['name']

            monthly_contribution = 0.0
            item = next((x for x in self.saving_items if x['name'] == etf_name), None)
            if item:
                monthly_contribution = item['target'] / 12.0

            values = [
                compound_interest_calculator(
                    current_value=start_value,
                    monthly_contribution=monthly_contribution,
                    annual_rate=annual_rate,
                    years=year - start_year
                )
                for year in years_list
            ]

            chart.plot(years_list, values, marker="dot", label=etf_name)

        chart.title("Portfolio Growth")
        chart.xlabel("Year")
        chart.ylabel("Value ($)")

        chart.show()

    def action_back(self):
        self.app.pop_screen()

# ------------------ Compound Interest Simulation Screen ------------------

class CompoundInterestSimulationScreen(Screen):
    BINDINGS = [("b", "back", "Back")]

    def __init__(self, market_data, simulation_data, saving_items: List[Dict]):
        super().__init__()
        self.market_data = market_data
        self.simulation_data = simulation_data
        self.saving_items = saving_items

    def compose(self) -> ComposeResult:
        yield Header()
        yield PlotextPlot(id="chart_area")
        yield Footer()

    def on_mount(self):
        self.draw_chart()

    def draw_chart(self):
        chart = self.query_one("#chart_area", PlotextPlot).plt

        etfs = self.market_data.get('etf', [])

        start_year = 2025
        until_year = self.simulation_data.get('until_year', 2050)
        years_count = until_year - start_year

        min_rate = self.simulation_data.get('min_annual_rate', -0.1)
        max_rate = self.simulation_data.get('max_annual_rate', 0.1)

        years_list = list(range(start_year, until_year + 1))
        runs = self.simulation_data.get('runs', 1)

        chart.clear_figure()

        for etf in etfs:
            start_value = etf['price']
            etf_name = etf['name']

            monthly_contribution = 0.0
            item = next((x for x in self.saving_items if x['name'] == etf_name), None)
            if item:
                monthly_contribution = item['target'] / 12.0

            all_paths = [
                monte_carlo_path(
                    start_value=start_value,
                    monthly_contribution=monthly_contribution,
                    years=years_count,
                    min_rate=min_rate,
                    max_rate=max_rate
                )
                for _ in range(runs)
            ]

            median_path = [statistics.median(values) for values in zip(*all_paths)]
            chart.plot(years_list, median_path, marker="dot", label=f"{etf_name} (median)")

        chart.title("Monte Carlo Portfolio Projection")
        chart.xlabel("Year")
        chart.ylabel("Value ($)")

        chart.show()

    def action_back(self):
        self.app.pop_screen()

# ------------------ Main App ------------------

class FinanceApp(App):
    BINDINGS = [("q", "quit", "Quit"), ("c", "compound", "Show Compound Interest"), ('s', "simulation", "Show Compound Interest Simulation")]
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
        data_path = os.path.join(os.path.dirname(__file__), 'finances.yml')
        with open(data_path, 'r') as f:
            self.data = yaml.safe_load(f)

        self.load_finances()

    def load_finances(self):
        data = self.data
        # Incomes tree
        incomes_tree = self.query_one("#incomes_tree", Tree)
        total_income = 0
        for income in data.get('incomes', []):
            income_value = yearly_adjusted_monthly_value(income)
            monthly = to_monthly(income_value, income['time'])
            incomes_tree.root.add_leaf(f"{income['name']}: {monthly:.2f}$ (weighted annual average)")
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
            items = saving.get('items', [])
            for item in items:
                monthly_cost = item['target'] / 12
                saving_tree.root.add_leaf(f"{item['name']}: {monthly_cost:.2f}$ (target: {item['target']}$)")
                monthly_saving_total += monthly_cost
            saving_tree.root.expand()

        net_balance = total_income - total_expense
        annual_net_balance = net_balance * 12
        net_balance_after_saving = net_balance - monthly_saving_total

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

    def action_compound(self):
        self.push_screen(CompoundInterestScreen(self.data['market'], self.data['simulation'], self.data['saving']['items']))

    def action_simulation(self):
        self.push_screen(CompoundInterestSimulationScreen(self.data['market'], self.data['simulation'], self.data['saving']['items']))

def main():
    FinanceApp().run()


if __name__ == "__main__":
    main()
