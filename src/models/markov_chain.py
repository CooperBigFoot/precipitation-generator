from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class MarkovChain:
    transition_matrix: pd.DataFrame = None

    def compute_transition_matrix(self, classified_data: np.ndarray) -> None:
        # Implementation to be added
        pass

    def generate_sequence(self, length: int) -> None:
        # Implementation to be added
        pass

    def save_transition_matrix(self, file_path: str) -> None:
        # Implementation to be added
        pass
