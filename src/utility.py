import random
from datetime import datetime
from typing import List

from src.model.etf import Etf
from src.model.saving import Saving
from src.model.income import Income
from src.time import Time


def to_monthly(value, time):
    if time == Time.DAY.value:
        return value * 30
    elif time == Time.MONTH.value:
        return value
    elif time == Time.ANNUAL.value:
        return value / 12
    else:
        return 0


def yearly_adjusted_monthly_value(income: Income) -> float:
    base_value = income.value
    time = income.time
    monthly_base = to_monthly(base_value, time)

    future_value = income.future_value
    future_date = income.future_date

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
    compounds_per_year: int = 12,
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


def monte_carlo_path(
    start_value: float,
    monthly_contribution: float,
    years: List[int],
    min_rate: float,
    max_rate: float,
) -> List[float]:
    value = start_value
    results = [value]

    for _ in years:
        r = random.uniform(min_rate, max_rate)

        for _ in range(12):
            value = value * (1 + r / 12) + monthly_contribution

        results.append(value)

    return results


def calculate_monthly_contribution(savings: List[Saving], etf: Etf) -> float:
    try:
        saving = next(s for s in savings if s.name.casefold() == etf.name.casefold())
        return saving.target / 12.0
    except StopIteration:
        return 0.0


def get_years(from_year: int, to_year: int) -> List[int]:
    return list(range(from_year, to_year + 1))


def get_years_from_now(to_year: int) -> List[int]:
    current_year: int = datetime.today().year
    return get_years(current_year, to_year)
