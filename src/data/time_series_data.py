import pandas as pd
from typing import Optional
from dataclasses import dataclass


@dataclass
class TimeSeriesData:
    """
    A class to handle time series data, specifically for precipitation data.

    Attributes:
        data (pd.DataFrame): The time series data stored as a pandas DataFrame.
    """

    data: Optional[pd.DataFrame] = None

    @classmethod
    def from_csv(cls, file_path: str):
        """
        Create a TimeSeriesData instance by reading data from a CSV file.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            TimeSeriesData: An instance of TimeSeriesData with loaded data.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            pd.errors.EmptyDataError: If the CSV file is empty.
            pd.errors.ParserError: If the CSV file is not properly formatted.
        """
        try:
            data = pd.read_csv(file_path, parse_dates=[0], index_col=0)
            if len(data.columns) < 1:
                raise ValueError(
                    "CSV file must have at least two columns: date and precipitation."
                )
            data.columns = [
                "precipitation"
            ]  # Rename the second column to 'precipitation'
            return cls(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {file_path} was not found.")
        except pd.errors.EmptyDataError:
            raise pd.errors.EmptyDataError(f"The file at {file_path} is empty.")
        except pd.errors.ParserError:
            raise pd.errors.ParserError(
                f"Error parsing the CSV file at {file_path}. Please check the file format."
            )

    def get_time_resolution(self) -> str:
        """
        Infer the time resolution of the data.

        Returns:
            str: The inferred time frequency as a string, or "Unknown" if it cannot be determined.

        Raises:
            ValueError: If the data attribute is None or has less than 2 entries.
        """
        if self.data is None or len(self.data) < 2:
            raise ValueError("Insufficient data to determine time resolution.")
        return pd.infer_freq(self.data.index) or "Unknown"

    def resample_data(self, frequency: str) -> "TimeSeriesData":
        """
        Create a new TimeSeriesData instance with data resampled to a new frequency.

        Args:
            frequency (str): The new time frequency (e.g., 'D' for daily, 'H' for hourly).

        Returns:
            TimeSeriesData: A new instance with resampled data.

        Raises:
            ValueError: If the data attribute is None.
        """
        if self.data is None:
            raise ValueError("No data available for resampling.")
        resampled_data = self.data.resample(frequency).mean()
        return TimeSeriesData(resampled_data)

    def filter_by_date_range(self, start_date: str, end_date: str) -> "TimeSeriesData":
        """
        Create a new TimeSeriesData instance with data filtered to a specific date range.

        Args:
            start_date (str): The start date of the range (inclusive).
            end_date (str): The end date of the range (inclusive).

        Returns:
            TimeSeriesData: A new instance with filtered data.

        Raises:
            ValueError: If the data attribute is None.
            ValueError: If the specified date range is invalid.
        """
        if self.data is None:
            raise ValueError("No data available for filtering.")
        try:
            filtered_data = self.data.loc[start_date:end_date]
            return TimeSeriesData(filtered_data)
        except KeyError:
            raise ValueError(f"Invalid date range: {start_date} to {end_date}")

    def get_precipitation_series(self) -> Optional[pd.Series]:
        """
        Extract the precipitation data series from the time series data.

        Returns:
            Optional[pd.Series]: The precipitation data as a pandas Series, or None if not available.

        Raises:
            ValueError: If the data attribute is None.
            KeyError: If the 'precipitation' column is not present in the data.
        """
        if self.data is None:
            raise ValueError("No data available.")
        try:
            return self.data["precipitation"]
        except KeyError:
            raise KeyError("No 'precipitation' column found in the data.")

    def plot(self) -> None:
        """
        Plot the time series data.

        Raises:
            ValueError: If the data attribute is None.
            ImportError: If matplotlib is not installed.
        """
        if self.data is None:
            raise ValueError("No data available for plotting.")
        try:
            self.data.plot()
        except ImportError:
            raise ImportError("Matplotlib is required for plotting. Please install it.")
