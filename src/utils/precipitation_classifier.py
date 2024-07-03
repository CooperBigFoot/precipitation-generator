from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict


@dataclass
class PrecipitationClassifier:
    categories: List[str] = field(
        default_factory=lambda: ["very_dry", "dry", "normal", "wet", "very_wet"]
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
        seasonal_data = self._get_seasonal_data(data)
        classified_data = pd.DataFrame(index=data.columns, columns=self.seasons.keys())

        for season, season_data in seasonal_data.items():
            percentiles = np.linspace(0, 100, len(self.categories) + 1)[1:-1]
            thresholds = np.percentile(season_data.values, percentiles)

            def classify_value(value):
                for i, threshold in enumerate(thresholds):
                    if value <= threshold:
                        return self.categories[i]
                return self.categories[-1]

            classified_data[season] = season_data.apply(classify_value)

        return classified_data

    def _get_seasonal_data(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        seasonal_data = {}
        for season, months in self.seasons.items():
            season_mask = data.index.month.isin(months)
            seasonal_data[season] = data[season_mask].sum()
        return seasonal_data

    def plot_classification_distribution(self, classified_data: pd.DataFrame) -> None:
        fig, axes = plt.subplots(2, 2, figsize=(12, 12))
        fig.suptitle("Distribution of Precipitation Classifications by Season")

        colors = plt.cm.get_cmap("Set3")(np.linspace(0, 1, len(self.categories)))

        for idx, season in enumerate(self.seasons.keys()):
            ax = axes[idx // 2, idx % 2]
            class_counts = classified_data[season].value_counts().sort_index()
            class_counts.plot(kind="bar", ax=ax, color=colors)
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
        seasonal_data = self._get_seasonal_data(data)

        fig, axes = plt.subplots(2, 2, figsize=(12, 12))
        fig.suptitle(
            "Distribution of Seasonal Precipitation with Classification Thresholds"
        )

        for idx, (season, season_data) in enumerate(seasonal_data.items()):
            ax = axes[idx // 2, idx % 2]
            percentiles = np.linspace(0, 100, len(self.categories) + 1)[1:-1]
            thresholds = np.percentile(season_data.values, percentiles)

            ax.hist(season_data, bins=30, edgecolor="black", alpha=0.7)
            ax.set_title(season)
            ax.set_xlabel("Total Precipitation (mm/season)")
            ax.set_ylabel("Number of Simulations")

            for i, threshold in enumerate(thresholds):
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
        classified_data.to_csv(file_path)

    @staticmethod
    def load_classified_data(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path, index_col=0)
