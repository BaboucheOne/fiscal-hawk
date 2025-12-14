from src.model.simulation import Simulation


class SimulationController:
    def __init__(self, simulation: Simulation):
        self.__simulation = simulation

    @property
    def simulation(self) -> Simulation:
        return self.__simulation