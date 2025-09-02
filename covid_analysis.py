import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def fetch_global_data():
    """Fetch global Covid-19 summary data."""
    url = "https://disease.sh/v3/covid-19/all"
    response = requests.get(url)
    if (status_ok := response.status_code == 200):
        return response.json()
    print("Error fetching global data")
    return None

def fetch_historical_data(days=30):
    """Fetch historical Covid-19 data for the last 'days' days."""
    url = f"https://disease.sh/v3/covid-19/historical/all?lastdays={days}"
    response = requests.get(url)
    if (status_ok := response.status_code == 200):
        return response.json()
    print("Error fetching historical data")
    return None

def fetch_countries_data():
    """Fetch Covid-19 data for all countries."""
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    if (status_ok := response.status_code == 200):
        return response.json()
    print("Error fetching countries data")
    return None

def main():
    print("Fetching Covid-19 data...")

    # Global summary
    global_data = fetch_global_data()
    if global_data is None:
        return
    print("\nGlobal Summary:")
    print(f"Total Cases: {global_data['cases']:,}")
    print(f"Total Deaths: {global_data['deaths']:,}")
    print(f"Total Recovered: {global_data['recovered']:,}")
    print(f"Active Cases: {global_data['active']:,}")

    # Historical data
    hist_data = fetch_historical_data(30)
    if hist_data is None:
        return
    cases = hist_data['cases']
    deaths = hist_data['deaths']
    recovered = hist_data['recovered']

    df = pd.DataFrame({
        'date': list(cases.keys()),
        'cases': list(cases.values()),
        'deaths': list(deaths.values()),
        'recovered': list(recovered.values())
    })
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # Calculate daily new cases
    df['new_cases'] = df['cases'].diff()

    print("\nHistorical Data (Last 30 Days):")
    print(df.tail())

    # Visualization
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(df['date'], df['cases'], color='blue')
    plt.title('Total Cases Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cases')
    plt.xticks(rotation=45)

    plt.subplot(2, 2, 2)
    plt.plot(df['date'], df['new_cases'], color='orange')
    plt.title('Daily New Cases')
    plt.xlabel('Date')
    plt.ylabel('New Cases')
    plt.xticks(rotation=45)

    plt.subplot(2, 2, 3)
    plt.plot(df['date'], df['deaths'], color='red')
    plt.title('Total Deaths Over Time')
    plt.xlabel('Date')
    plt.ylabel('Deaths')
    plt.xticks(rotation=45)

    plt.subplot(2, 2, 4)
    plt.plot(df['date'], df['recovered'], color='green')
    plt.title('Total Recovered Over Time')
    plt.xlabel('Date')
    plt.ylabel('Recovered')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('covid_trends.png')
    print("\nVisualization saved as 'covid_trends.png'")

    # Countries data for top 10
    countries_data = fetch_countries_data()
    if countries_data is None:
        return
    countries_df = pd.DataFrame(countries_data)
    top_countries = countries_df.nlargest(10, 'cases')[['country', 'cases', 'deaths', 'recovered']]

    print("\nTop 10 Countries by Cases:")
    print(top_countries)

    # Bar chart for top countries
    plt.figure(figsize=(10, 6))
    plt.bar(top_countries['country'], top_countries['cases'], color='skyblue')
    plt.title('Top 10 Countries by Total Cases')
    plt.xlabel('Country')
    plt.ylabel('Cases')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('top_countries.png')
    print("Top countries chart saved as 'top_countries.png'")

    # Basic correlation example (if vaccination data available, but for now, cases vs deaths)
    correlation = df['cases'].corr(df['deaths'])
    print(f"\nCorrelation between total cases and deaths: {correlation:.2f}")

if __name__ == "__main__":
    main()
