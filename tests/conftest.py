"""Configuration and fixtures for pandas-marc tests."""

import os

import pandas as pd
from pymarc import MARCReader
import pytest


@pytest.fixture(scope='session')
def tests_path():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope='session')
def dataframe(tests_path):
    dataframe_path = os.path.join(tests_path, 'fixtures/dataframe.csv')
    dataframe = pd.read_csv(dataframe_path, dtype=str)
    dataframe = dataframe.fillna('')
    return dataframe


@pytest.fixture(scope='session')
def records(tests_path):
    records_path = os.path.join(tests_path, 'fixtures/records.mrc')
    with open(records_path, 'rb') as records_file:
        reader = MARCReader(records_file)
        return list(reader)
