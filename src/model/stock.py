from dataclasses import dataclass


@dataclass
class Stock:
    symbol: str
    quantity: float

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError(f"quantity ({self.quantity}) must be positive")
