from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict


@dataclass
class PrecipitationClassifier:
    categories: List[str] = field(
        default_factory=lambda: ["very_dry", "dry", "wet", "very_wet"]
    )
    seasons: Dict[str, List[int]] = field(
        default_factory=lambda: {
            "Winter": [12, 1, 2],
            "Spring": [3, 4, 5],
            "Summer": [6, 7, 8],
            "Fall": [9, 10, 11],
        }
    )

    def classify_precipitation(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Classify precipitation data for each season in each simulation based on quartiles.

        Args:
            data (pd.DataFrame): DataFrame with date index and precipitation data in columns.
                                 Each column represents a different simulation.

        Returns:
            pd.DataFrame: DataFrame where each row represents a simulation, and columns
                          represent classifications for each season.
        """
        seasonal_data = self._get_seasonal_data(data)
        classified_data = pd.DataFrame(index=data.columns, columns=self.seasons.keys())

        for season, season_data in seasonal_data.items():
            quartiles = np.percentile(season_data.values, [25, 50, 75])

            def classify_value(value):
                if value <= quartiles[0]:
                    return self.categories[0]  # very_dry
                elif value <= quartiles[1]:
                    return self.categories[1]  # dry
                elif value <= quartiles[2]:
                    return self.categories[2]  # wet
                else:
                    return self.categories[3]  # very_wet

            classified_data[season] = season_data.apply(classify_value)

        return classified_data

    def _get_seasonal_data(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Calculate total precipitation for each season in each simulation.

        Args:
            data (pd.DataFrame): Original precipitation data.

        Returns:
            Dict[str, pd.Series]: Dictionary with seasons as keys and Series of seasonal totals as values.
        """
        seasonal_data = {}
        for season, months in self.seasons.items():
            season_mask = data.index.month.isin(months)
            seasonal_data[season] = data[season_mask].sum()
        return seasonal_data

    def plot_classification_distribution(self, classified_data: pd.DataFrame) -> None:
        """
        Plot the distribution of precipitation classifications for each season.

        Args:
            classified_data (pd.DataFrame): The classified precipitation data.
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 15))
        fig.suptitle("Distribution of Precipitation Classifications by Season")

        colors = {
            "very_dry": "#FFA07A",
            "dry": "#98FB98",
            "wet": "#87CEFA",
            "very_wet": "#9370DB",
        }

        for idx, season in enumerate(self.seasons.keys()):
            ax = axes[idx // 2, idx % 2]
            class_counts = classified_data[season].value_counts().sort_index()
            class_counts.plot(
                kind="bar", ax=ax, color=[colors[cat] for cat in class_counts.index]
            )
            ax.set_title(season)
            ax.set_xlabel("Precipitation Class")
            ax.set_ylabel("Number of Simulations")
            ax.tick_params(axis="x", rotation=45)
            for i, v in enumerate(class_counts):
                ax.text(i, v, str(v), ha="center", va="bottom")

        plt.tight_layout()
        plt.subplots_adjust(top=0.93)
        plt.show()

    def plot_seasonal_precipitation_distribution(self, data: pd.DataFrame) -> None:
        """
        Plot the distribution of seasonal precipitation for all simulations with quartile thresholds.

        Args:
            data (pd.DataFrame): The original precipitation data.
        """
        seasonal_data = self._get_seasonal_data(data)

        fig, axes = plt.subplots(2, 2, figsize=(15, 15))
        fig.suptitle("Distribution of Seasonal Precipitation with Quartile Thresholds")

        for idx, (season, season_data) in enumerate(seasonal_data.items()):
            ax = axes[idx // 2, idx % 2]
            quartiles = np.percentile(season_data.values, [25, 50, 75])

            ax.hist(season_data, bins=30, edgecolor="black", alpha=0.7)
            ax.set_title(season)
            ax.set_xlabel("Total Precipitation (mm/season)")
            ax.set_ylabel("Number of Simulations")

            for i, threshold in enumerate(quartiles):
                ax.axvline(threshold, color="r", linestyle="--", linewidth=1)
                ax.text(
                    threshold,
                    ax.get_ylim()[1],
                    f" {self.categories[i]}|{self.categories[i+1]}",
                    rotation=90,
                    va="top",
                    fontsize=8,
                )

        plt.tight_layout()
        plt.subplots_adjust(top=0.93)
        plt.show()

    def save_classified_data(
        self, classified_data: pd.DataFrame, file_path: str
    ) -> None:
        """
        Save the classified precipitation data to a CSV file.

        Args:
            classified_data (pd.DataFrame): The classified precipitation data.
            file_path (str): The path where the CSV file will be saved.
        """
        classified_data.to_csv(file_path)

    @staticmethod
    def load_classified_data(file_path: str) -> pd.DataFrame:
        """
        Load previously classified precipitation data from a CSV file.

        Args:
            file_path (str): The path to the CSV file containing the classified data.

        Returns:
            pd.DataFrame: A DataFrame containing the loaded classified data.
        """
        return pd.read_csv(file_path, index_col=0)
