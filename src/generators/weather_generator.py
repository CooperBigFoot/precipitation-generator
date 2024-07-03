from dataclasses import dataclass, field
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Union


@dataclass
class WeatherGenerator:
    synthetic_data: pd.DataFrame
    classified_data: pd.DataFrame
    seasons: Dict[str, List[int]] = field(
        default_factory=lambda: {
            "Winter": [12, 1, 2],
            "Spring": [3, 4, 5],
            "Summer": [6, 7, 8],
            "Fall": [9, 10, 11],
        }
    )

    def generate_weather(
        self,
        year_structure: Union[List[Tuple[str, str]], List[List[Tuple[str, str]]]],
        num_years: int = 1,
    ) -> pd.DataFrame:
        """
        Generate weather scenarios based on the provided year structure.

        Args:
            year_structure (Union[List[Tuple[str, str]], List[List[Tuple[str, str]]]]):
                Either a single year structure or a list of year structures for multiple years.
            num_years (int): Number of years to generate if a single year structure is provided.
                             Ignored if a multi-year structure is provided. Default is 1.

        Returns:
            pd.DataFrame: Generated weather scenario with simulated days.

        Raises:
            ValueError: If the input parameters are invalid.
        """
        scenario = []

        # Check if we have a multi-year structure
        if isinstance(year_structure[0], list):
            if num_years != 1:
                print(
                    "Warning: num_years is ignored when a multi-year structure is provided."
                )
            for year in year_structure:
                for season, condition in year:
                    segment = self._select_matching_segment(season, condition)
                    scenario.extend(segment)
        else:
            if num_years < 1:
                raise ValueError(
                    "num_years must be at least 1 for a single year structure."
                )
            for _ in range(num_years):
                for season, condition in year_structure:
                    segment = self._select_matching_segment(season, condition)
                    scenario.extend(segment)

        # Create a range of simulated days
        simulated_days = range(1, len(scenario) + 1)

        # Create the DataFrame with simulated days
        scenario_df = pd.DataFrame(
            {"simulated_day": simulated_days, "precipitation": scenario}
        )

        # Set 'simulated_day' as the index
        scenario_df.set_index("simulated_day", inplace=True)

        return scenario_df

    def _select_matching_segment(self, season: str, condition: str) -> List[float]:
        """
        Select a matching segment from synthetic_data based on the season and condition.

        Args:
            season (str): The season for which to select data.
            condition (str): The precipitation condition (e.g., 'wet', 'dry').

        Returns:
            List[float]: A list of precipitation values for the selected segment.
        """
        # Filter classified data for the given season and condition
        matching_simulations = self.classified_data[
            (self.classified_data[season] == condition)
        ].index

        if len(matching_simulations) == 0:
            raise ValueError(
                f"No matching simulations found for {season} - {condition}"
            )

        # Randomly select one of the matching simulations
        selected_simulation = np.random.choice(matching_simulations)

        # Get the corresponding synthetic data
        simulation_data = self.synthetic_data[selected_simulation]

        # Extract the seasonal segment
        season_months = self.seasons[season]
        seasonal_mask = simulation_data.index.month.isin(season_months)
        seasonal_segment = simulation_data[seasonal_mask].tolist()

        return seasonal_segment

    def save_scenario(self, scenario: pd.DataFrame, file_path: str) -> None:
        """
        Save the generated scenario to a CSV file.

        Args:
            scenario (pd.DataFrame): The generated weather scenario.
            file_path (str): The path where the CSV file will be saved.
        """
        scenario.to_csv(file_path)

    @staticmethod
    def load_scenario(file_path: str) -> pd.DataFrame:
        """
        Load a previously generated scenario from a CSV file.

        Args:
            file_path (str): The path to the CSV file containing the scenario.

        Returns:
            pd.DataFrame: The loaded weather scenario.
        """
        return pd.read_csv(file_path, index_col="simulated_day")
