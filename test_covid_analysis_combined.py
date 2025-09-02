import pytest
import covid_analysis
import pandas as pd
from unittest.mock import patch, Mock

def test_fetch_global_data_success():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'cases': 100, 'deaths': 10, 'recovered': 90, 'active': 5}
    with patch('covid_analysis.requests.get', return_value=mock_response):
        data = covid_analysis.fetch_global_data()
        assert data['cases'] == 100
        assert data['deaths'] == 10

def test_fetch_global_data_failure():
    mock_response = Mock()
    mock_response.status_code = 500
    with patch('covid_analysis.requests.get', return_value=mock_response):
        data = covid_analysis.fetch_global_data()
        assert data is None

def test_fetch_historical_data_success():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'cases': {'2023-01-01': 100, '2023-01-02': 150},
        'deaths': {'2023-01-01': 5, '2023-01-02': 7},
        'recovered': {'2023-01-01': 50, '2023-01-02': 80}
    }
    with patch('covid_analysis.requests.get', return_value=mock_response):
        data = covid_analysis.fetch_historical_data()
        assert 'cases' in data
        assert 'deaths' in data

def test_fetch_historical_data_failure():
    mock_response = Mock()
    mock_response.status_code = 404
    with patch('covid_analysis.requests.get', return_value=mock_response):
        data = covid_analysis.fetch_historical_data()
        assert data is None

def test_fetch_countries_data_success():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{'country': 'Testland', 'cases': 1000, 'deaths': 50, 'recovered': 900}]
    with patch('covid_analysis.requests.get', return_value=mock_response):
        data = covid_analysis.fetch_countries_data()
        assert isinstance(data, list)
        assert data[0]['country'] == 'Testland'

def test_fetch_countries_data_failure():
    mock_response = Mock()
    mock_response.status_code = 403
    with patch('covid_analysis.requests.get', return_value=mock_response):
        data = covid_analysis.fetch_countries_data()
        assert data is None

def test_fetch_global_data_error_handling():
    mock_response = Mock()
    mock_response.status_code = 500
    with patch('covid_analysis.requests.get', return_value=mock_response):
        data = covid_analysis.fetch_global_data()
        assert data is None

def test_fetch_historical_data_error_handling():
    mock_response = Mock()
    mock_response.status_code = 404
    with patch('covid_analysis.requests.get', return_value=mock_response):
        data = covid_analysis.fetch_historical_data()
        assert data is None

def test_fetch_countries_data_error_handling():
    mock_response = Mock()
    mock_response.status_code = 403
    with patch('covid_analysis.requests.get', return_value=mock_response):
        data = covid_analysis.fetch_countries_data()
        assert data is None

def test_empty_historical_data():
    empty_data = {'cases': {}, 'deaths': {}, 'recovered': {}}
    with patch('covid_analysis.fetch_historical_data', return_value=empty_data):
        hist_data = covid_analysis.fetch_historical_data()
        df = pd.DataFrame({
            'date': list(hist_data['cases'].keys()),
            'cases': list(hist_data['cases'].values()),
            'deaths': list(hist_data['deaths'].values()),
            'recovered': list(hist_data['recovered'].values())
        })
        assert df.empty

def test_large_historical_data():
    large_data = {
        'cases': {f'2023-01-{str(i).zfill(2)}': i*1000 for i in range(1, 101)},
        'deaths': {f'2023-01-{str(i).zfill(2)}': i*10 for i in range(1, 101)},
        'recovered': {f'2023-01-{str(i).zfill(2)}': i*900 for i in range(1, 101)}
    }
    with patch('covid_analysis.fetch_historical_data', return_value=large_data):
        hist_data = covid_analysis.fetch_historical_data()
        df = pd.DataFrame({
            'date': list(hist_data['cases'].keys()),
            'cases': list(hist_data['cases'].values()),
            'deaths': list(hist_data['deaths'].values()),
            'recovered': list(hist_data['recovered'].values())
        })
        assert len(df) == 100

def test_visualization_files_created(tmp_path):
    import os
    import matplotlib.pyplot as plt

    # Patch savefig to save to tmp_path
    original_savefig = plt.savefig

    def savefig_patch(filename, *args, **kwargs):
        path = tmp_path / filename
        original_savefig(str(path), *args, **kwargs)

    plt.savefig = savefig_patch

    # Run main to generate plots
    covid_analysis.main()

    # Check files exist
    covid_trends = tmp_path / 'covid_trends.png'
    top_countries = tmp_path / 'top_countries.png'
    assert covid_trends.exists()
    assert top_countries.exists()

    # Restore original savefig
    plt.savefig = original_savefig
