from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class TimeSeriesData:
    data: Optional[pd.DataFrame] = None

    @classmethod
    def from_csv(cls, file_path: str):
        # Implementation to be added
        pass

    def load_data(self, file_path: str) -> None:
        # Implementation to be added
        pass

    def get_time_resolution(self) -> str:
        # Implementation to be added
        pass

    def resample_data(self, frequency: str) -> None:
        # Implementation to be added
        pass

    def filter_by_date_range(self, start_date: str, end_date: str) -> None:
        # Implementation to be added
        pass

    def get_precipitation_series(self):
        # Implementation to be added
        pass

    def plot(self) -> None:
        # Implementation to be added
        pass
