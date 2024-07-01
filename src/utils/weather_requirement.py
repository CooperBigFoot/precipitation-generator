from dataclasses import dataclass


@dataclass
class WeatherRequirement:
    season: str
    condition: str
    intensity: float
