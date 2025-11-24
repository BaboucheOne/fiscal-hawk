from typing import List, Dict

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual_plotext import PlotextPlot

from src.utility import compound_interest_calculator


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

        etfs = self.market_data.get("etf", [])

        start_year = 2025
        until_year = self.simulation_data.get("until_year", 2050)
        annual_rate = self.simulation_data.get("annual_rate", 0.1)
        years_list = list(range(start_year, until_year + 1))

        chart.clear_figure()

        for etf in etfs:
            start_value = etf["price"]
            etf_name = etf["name"]

            monthly_contribution = 0.0
            item = next((x for x in self.saving_items if x["name"] == etf_name), None)
            if item:
                monthly_contribution = item["target"] / 12.0

            values = [
                compound_interest_calculator(
                    current_value=start_value,
                    monthly_contribution=monthly_contribution,
                    annual_rate=annual_rate,
                    years=year - start_year,
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
