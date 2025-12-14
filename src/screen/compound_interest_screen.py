from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual_plotext import PlotextPlot

from src.controller.account_controller import AccountController
from src.controller.simulation_controller import SimulationController
from src.service_locator import ServiceLocator
from src.utility import compound_interest_calculator


class CompoundInterestScreen(Screen):
    BINDINGS = [("b", "back", "Back")]

    def __init__(self):
        super().__init__()

        self.__account_controller: AccountController = ServiceLocator.get_dependency(
            AccountController
        )
        self.__simulation_controller: SimulationController = (
            ServiceLocator.get_dependency(SimulationController)
        )

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
        annual_rate = self.__simulation_controller.simulation.max_annual_rate
        years_list = list(range(start_year, until_year + 1))

        chart.clear_figure()

        for etf in self.__account_controller.market.etfs:
            start_value = etf.price
            etf_name = etf.name

            monthly_contribution = 0.0
            saving = next(
                (
                    saving
                    for saving in self.__account_controller.saving_configuration.savings
                    if saving.name.lower() == etf_name.lower()
                ),
                None,
            )
            if saving:
                monthly_contribution = saving.target / 12.0

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
