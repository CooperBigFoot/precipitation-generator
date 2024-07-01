from dataclasses import dataclass
import pandas as pd


@dataclass
class MarkovChain:
    transition_matrix: pd.DataFrame = None

    def fit(self, data: pd.DataFrame) -> None:
        pass

    def generate_sequence(self, length: int) -> None:
        pass
