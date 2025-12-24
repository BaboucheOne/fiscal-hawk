from dataclasses import dataclass


@dataclass
class Saving:
    name: str
    target: float

    def __post_init__(self):
        if self.target <= 0:
            raise ValueError(f"target ({self.target}) must be positive.")
