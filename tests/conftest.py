"""Configuration and fixtures for pandas-marc tests."""

import pandas as pd
from pymarc import MARCReader
import pytest


@pytest.fixture(scope='session')
def dataframe():
    dataframe = pd.read_csv('tests/fixtures/dataframe.csv', dtype=str)
    dataframe = dataframe.fillna('')
    return dataframe


@pytest.fixture(scope='session')
def records():
    with open('tests/fixtures/records.mrc', 'rb') as records_file:
        reader = MARCReader(records_file)
        return list(reader)
