from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class TimeSeriesData:
    data: Optional[pd.DataFrame] = None

    def load_data(self, file_path: str) -> None:
        pass

    def get_time_resolution(self) -> str:
        pass
