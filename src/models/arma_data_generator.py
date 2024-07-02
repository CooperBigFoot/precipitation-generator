from dataclasses import dataclass
from typing import Tuple
import pandas as pd


@dataclass
class ARMADataGenerator:
    order: Tuple[int, int]
    steps: int
    model = None

    def fit(self, time_series: pd.Series) -> None:
        # Implementation to be added
        pass

    def generate(self, n_trajectories: int):
        # Implementation to be added
        pass

    def save_generated_trajectories(self, file_path: str) -> None:
        # Implementation to be added
        pass
