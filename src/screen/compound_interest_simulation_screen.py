import statistics

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual_plotext import PlotextPlot

from src.controller.account_controller import AccountController
from src.controller.simulation_controller import SimulationController
from src.model.saving import Saving
from src.utility import monte_carlo_path


class CompoundInterestSimulationScreen(Screen):
    BINDINGS = [("b", "back", "Back")]

    def __init__(self, account_controller: AccountController, simulation_controller: SimulationController):
        super().__init__()

        self.__account_controller: AccountController = account_controller
        self.__simulation_controller: SimulationController = simulation_controller

    def compose(self) -> ComposeResult:
        yield Header()
        yield PlotextPlot(id="chart_area")
        yield Footer()

    def on_mount(self):
        self.draw_chart()

    def draw_chart(self):
        chart = self.query_one("#chart_area", PlotextPlot).plt

        start_year = 2025
        until_year = self.__simulation_controller.simulation.until_year
        years_count = until_year - start_year

        min_rate = self.__simulation_controller.simulation.min_annual_rate
        max_rate = self.__simulation_controller.simulation.max_annual_rate

        years_list = list(range(start_year, until_year + 1))
        runs = self.__simulation_controller.simulation.runs

        chart.clear_figure()

        for etf in self.__account_controller.market.etfs:
            start_value = etf.price
            etf_name = etf.name

            monthly_contribution = 0.0
            saving: Saving = next((saving for saving in self.__account_controller.saving_configuration.savings if saving.name.lower() == etf_name.lower()), None)
            if saving:
                monthly_contribution = saving.target / 12.0

            all_paths = [
                monte_carlo_path(
                    start_value=start_value,
                    monthly_contribution=monthly_contribution,
                    years=years_count,
                    min_rate=min_rate,
                    max_rate=max_rate,
                )
                for _ in range(runs)
            ]

            median_path = [statistics.median(values) for values in zip(*all_paths)]
            chart.plot(
                years_list, median_path, marker="dot", label=f"{etf_name} (median)"
            )

        chart.title("Monte Carlo Portfolio Projection")
        chart.xlabel("Year")
        chart.ylabel("Value ($)")

        chart.show()

    def action_back(self):
        self.app.pop_screen()
