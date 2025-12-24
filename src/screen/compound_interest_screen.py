from typing import List

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual_plotext import PlotextPlot

from src.controller.account_controller import AccountController
from src.controller.simulation_controller import SimulationController
from src.service_locator import ServiceLocator


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
        chart.clear_figure()

        years_list = self.__simulation_controller.get_years_from_now()

        for etf in self.__account_controller.market.etfs:
            values: List[float] = (
                self.__simulation_controller.simulate_compound_interest_on_etf(etf)
            )
            chart.plot(years_list, values, marker="dot", label=etf.name)

        chart.title("Portfolio Growth")
        chart.xlabel("Year")
        chart.ylabel("Value ($)")

        chart.show()

    def action_back(self):
        self.app.pop_screen()
