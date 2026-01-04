from dataclasses import dataclass


@dataclass
class Etf:
    symbol: str
    price: float
    quantity: float

    def __post_init__(self):
        if self.price < 0:
            raise ValueError(f"price ({self.price}) must be positive")

        if self.quantity < 0:
            raise ValueError(f"quantity ({self.quantity}) must be positive")
