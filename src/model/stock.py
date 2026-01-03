from dataclasses import dataclass


@dataclass
class Stock:
    name: str
    quantity: float

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError(f"quantity ({self.quantity}) must be positive")
