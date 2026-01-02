from dataclasses import dataclass
from datetime import date
from typing import List, Optional, get_origin, Union, get_args

import yaml

from src.model.expense import Expense
from src.model.income import Income
from src.model.market import Market
from src.model.planned_expense import PlannedExpense
from src.model.saving_configuration import SavingConfiguration
from src.model.simulation import Simulation


@dataclass
class Root:
    incomes: List[Income]
    planned_expenses: List[PlannedExpense]
    expenses: List[Expense]
    saving_configuration: SavingConfiguration
    market: Market
    simulation: Simulation

    @staticmethod
    def from_dict(data_class, data):
        origin = get_origin(data_class)

        if origin is Union:
            inner_types = [t for t in get_args(data_class) if t is not type(None)]
            inner_type = inner_types[0] if inner_types else None

            if data is None:
                return None

            return Root.from_dict(inner_type, data)

        if isinstance(data, list):
            inner_type = data_class.__args__[0]
            return [Root.from_dict(inner_type, item) for item in data]

        if isinstance(data, dict):
            kwargs = {}
            for key, field_type in data_class.__annotations__.items():
                if key in data:
                    kwargs[key] = Root.from_dict(field_type, data[key])
            return data_class(**kwargs)

        if data_class is date and isinstance(data, str):
            parts = data.split("-")
            if len(parts) == 2:
                year, month = map(int, parts)
                return date(year, month, 1)
            return date.fromisoformat(data)

        return data

    @classmethod
    def load(cls, path: str) -> "Root":
        with open(path, "r") as f:
            raw = yaml.safe_load(f)
        return cls.from_dict(cls, raw)
