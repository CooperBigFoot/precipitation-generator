from dataclasses import dataclass, field
from typing import Tuple
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA


@dataclass
class ARMADataGenerator:
    order: Tuple[int, int]  # (p, q) for ARMA
    steps: int
    model: ARIMA = field(init=False, default=None)

    def fit(self, time_series: pd.Series) -> None:
        """
        Fit the ARMA model to the given time series data.

        Args:
            time_series (pd.Series): The input time series data to fit the model to.
        """
        p, q = self.order
        self.model = ARIMA(time_series, order=(p, 0, q)).fit()

    def generate(self, n_trajectories: int) -> pd.DataFrame:
        """
        Generate multiple trajectories using the fitted ARMA model.

        Args:
            n_trajectories (int): The number of trajectories to generate.

        Returns:
            pd.DataFrame: A DataFrame containing the generated trajectories.
                          Each column represents a trajectory, and the index represents the time steps.

        Raises:
            ValueError: If the model hasn't been fitted yet.
        """
        if self.model is None:
            raise ValueError("Model has not been fitted. Call fit() method first.")

        simulations = []
        for _ in range(n_trajectories):
            sim = self.model.simulate(self.steps)
            simulations.append(sim)

        # Create a DataFrame with simulations as columns
        df = pd.concat(simulations, axis=1)
        df.columns = [f"Sim_{i+1}" for i in range(n_trajectories)]

        return df

    def save_generated_trajectories(self, data: pd.DataFrame, file_path: str) -> None:
        """
        Save the generated trajectories to a CSV file.

        Args:
            data (pd.DataFrame): The DataFrame containing the generated trajectories.
            file_path (str): The path where the CSV file will be saved.
        """
        data.to_csv(file_path)

    @staticmethod
    def load_generated_trajectories(file_path: str) -> pd.DataFrame:
        """
        Load previously generated trajectories from a CSV file.

        Args:
            file_path (str): The path to the CSV file containing the trajectories.

        Returns:
            pd.DataFrame: A DataFrame containing the loaded trajectories.
        """
        return pd.read_csv(file_path, index_col=0, parse_dates=True)
