# Covid-19 Data Analysis Project

This project analyzes real-time Covid-19 data using Python. It collects data on cases, recoveries, and fatalities from public APIs, processes it with Pandas and NumPy, and visualizes trends and patterns using Matplotlib.

## Features

- Fetches global Covid-19 summary data
- Retrieves historical data for trend analysis (last 30 days by default)
- Displays top 10 countries by total cases
- Generates visualizations:
  - Time series plots for cases, deaths, recoveries
  - Daily new cases
  - Bar chart for top countries
- Calculates basic correlations (e.g., cases vs deaths)

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Setup

1. Clone or download the project files.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```
python covid_analysis.py
```

The script will:
- Fetch data from the disease.sh API
- Print summary statistics to the console
- Generate and save visualization images (`covid_trends.png`, `top_countries.png`)

## Data Sources

- Global and historical data: [disease.sh](https://disease.sh/)
- Countries data: [disease.sh/v3/covid-19/countries](https://disease.sh/v3/covid-19/countries)

## Future Enhancements

- Add vaccination data analysis
- Implement predictive models for case forecasting
- Include lockdown impact analysis (requires additional data sources)
- Create interactive dashboards with Plotly or Dash

## License

This project is for educational purposes. Data is sourced from public APIs.
