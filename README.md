# Precipitation Generator

## Project Overview

This project aims to create a Python-based synthetic precipitation data generator that simulates weather patterns with specific conditions, such as a very dry summer or a wet spring. The system uses an ARMA (Autoregressive Moving Average) model to generate base synthetic data, which is then classified and assembled to meet user-defined weather scenarios. The code is designed to be flexible enough to handle different time resolutions and potentially include additional weather variables like temperature in the future.

## Components

### 1. Time Series Data Handling
- **TimeSeriesData**: A class encapsulating the entire precipitation DataFrame, providing methods for data manipulation, analysis, and visualization.

### 2. ARMA Data Generation
- **ARMADataGenerator**: Responsible for fitting an ARMA model to historical data and generating synthetic precipitation data.

### 3. Precipitation Classification
- **PrecipitationClassifier**: Classifies the synthetic data into categories (e.g., very dry, dry, normal, wet, very wet) for each season.

### 4. Custom Year Creation
- **CustomYearCreator**: Allows users to define custom year structures with specific seasonal conditions.

### 5. Weather Generation
- **WeatherGenerator**: Assembles the final weather scenarios by selecting appropriate data segments based on the user-defined structure.

### 6. Weather Requirements
- **WeatherRequirement**: A utility class for defining seasonal weather conditions.

## Key Features
- Flexible data handling with support for various time resolutions.
- ARMA model-based synthetic data generation.
- Seasonal classification of precipitation data.
- User-defined custom year structures for weather scenario creation.
- Efficient assembly of weather scenarios from pre-generated and classified data.

## Usage Example

```python
# Load and prepare data
historical_data = TimeSeriesData.from_csv('historical_data.csv')
arma_generator = ARMADataGenerator(order=(2,0), steps=365*10)
arma_generator.fit(historical_data.get_precipitation_series())
synthetic_data = arma_generator.generate(n_trajectories=100)

# Classify data
classifier = PrecipitationClassifier()
classified_data = classifier.classify_precipitation(synthetic_data)

# Create custom year structure
custom_year_creator = CustomYearCreator()
year_structure = custom_year_creator.create_custom_year_structure([
    ('Winter', 'wet'),
    ('Spring', 'dry'),
    ('Summer', 'very_dry'),
    ('Fall', 'normal')
])

# Generate weather scenario
weather_gen = WeatherGenerator(synthetic_data, classified_data)
scenario = weather_gen.generate_weather(year_structure, num_years=1)

# Analyze and visualize results
# (Add your analysis and visualization code here)
```

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
│   │   └── arma_data_generator.py
│   ├── generators/
│   │   ├── __init__.py
│   │   └── weather_generator.py
│   └── utils/
│       ├── __init__.py
│       ├── weather_requirement.py
│       ├── precipitation_classifier.py
│       └── custom_year_creator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_time_series_data.py
│   ├── test_arma_data_generator.py
│   ├── test_weather_generator.py
│   ├── test_precipitation_classifier.py
│   └── test_custom_year_creator.py
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
```

## Future Considerations
- Incorporate additional weather variables (e.g., temperature) into the model.
- Develop a Streamlit app for a user-friendly interface and visualization components.
- Implement advanced validation techniques to ensure the realism of generated scenarios.
- Expand the system to handle more complex user inputs and requirements.

## Installation and Setup
(Add instructions for setting up the project, including required dependencies)

## Contributing
(Add guidelines for contributing to the project)

## License
(Specify the license under which this project is released)