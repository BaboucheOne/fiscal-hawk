from dataclasses import dataclass


@dataclass
class Etf:
    name: str
    price: float

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError(f"price ({self.price}) must be positive")
