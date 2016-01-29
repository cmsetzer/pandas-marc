#!/usr/bin/env python3

"""Test suite for pandas-marc."""

from pandas_marc import MARCDataFrame


def test_instantiate_marcdataframe(dataframe):
    kwargs = {
        'dataframe': dataframe,
        'occurrence_delimiter': '|',
        'subfield_delimiter': '‡'
    }
    mdf = MARCDataFrame(**kwargs)
    for key, value in kwargs.items():
        assert getattr(mdf, key) is value


def test_marcdataframe_produces_correct_marc_records(dataframe, records):
    mdf = MARCDataFrame(dataframe)
    output = [record.as_marc() for record in mdf.records]
    expected = [record.as_marc() for record in records]
    assert output == expected
