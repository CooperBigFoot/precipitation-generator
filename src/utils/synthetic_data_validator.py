from dataclasses import dataclass
from typing import List
import pandas as pd
from .weather_requirement import WeatherRequirement


@dataclass
class SyntheticDataValidator:
    def validate(
        self, data: pd.DataFrame, requirements: List[WeatherRequirement]
    ) -> bool:
        # Implementation to be added
        pass
