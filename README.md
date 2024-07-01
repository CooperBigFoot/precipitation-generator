# Precipitation Generator

## Project Overview

This project aims to create a Python-based synthetic precipitation data generator that uses a Markov chain model to simulate weather patterns with specific conditions, such as a very dry summer or a wet spring. The code is designed to be flexible enough to handle different time resolutions and potentially include additional weather variables like temperature in the future.

## Components

### 1. Time Series Representation
- **Pandas DataFrame**: The primary structure for handling the time series data. It includes at least two columns: `date` and `precipitation`.
- **Flexibility**: The design accommodates various time resolutions, starting with daily data.

### 2. Data Classes and Structure
- **PrecipitationData**: A data class representing individual entries in the time series, containing `date` and `precipitation` attributes.
- **TimeSeriesData**: A class to encapsulate the entire DataFrame, providing methods for manipulation and analysis.

### 3. Markov Chain Model
- **MarkovChain**: A class responsible for building and using a Markov chain based on the historical precipitation data. It includes methods to fit the model to the data and generate new sequences.
- **Transition Matrix**: The core component of the Markov chain, representing the probabilities of transitioning between different states (precipitation levels).

### 4. Synthetic Data Generation
- **SyntheticDataGenerator**: A class utilizing the Markov chain to create synthetic precipitation data that meets specific criteria (e.g., dry summers, wet springs). It offers flexibility for future expansion to include additional parameters like temperature.

### 5. User Requirements and Flexibility
- The system allows users to specify conditions for the generated data, such as the dryness of a summer or the wetness of a spring. The exact method for specifying these requirements will be refined later.
- The codebase follows a mix of object-oriented and functional programming paradigms to ensure maintainability and scalability.

## Future Considerations
- Incorporate additional weather variables (e.g., temperature) into the model.
- Develop a Streamlit app for a user-friendly interface and visualization components.
- Expand the data generation logic to handle more complex user inputs and requirements.

## Project Structure

```plaintext
precipitation_generator/
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── time_series_data.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── markov_chain.py
│   ├── generators/
│   │   ├── __init__.py
│   │   └── precipitation_generator.py
│   └── utils/
│       ├── __init__.py
│       ├── weather_requirement.py
│       └── synthetic_data_validator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_time_series_data.py
│   ├── test_markov_chain.py
│   ├── test_precipitation_generator.py
│   └── test_synthetic_data_validator.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── exploration.ipynb
│
├── config/
│   └── config.yaml
│
├── requirements.txt
├── setup.py
├── README.md
└── .gitignore
