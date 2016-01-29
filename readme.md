pandas-marc
-----------

pandas-marc is a lightweight Python library for working with [MARC 21] bibliographic metadata using [pandas] dataframes. It uses [pymarc] for serializing to and deserializing from MARC.

[MARC 21]: https://www.loc.gov/marc/bibliographic/
[pandas]: http://pandas.pydata.org/
[pymarc]: https://github.com/edsu/pymarc/

### Quickstart

Let's say we have a CSV file with some tabular bibliographic metadata:

| MARC 007 | title                           |
| -------- | ------------------------------- |
| ta       | Woman in the nineteenth century |
| ta       | The fire next time              |

Using pandas, we can load in the CSV and prepare it for processing into MARC:

```python
import pandas as pd

dataframe = pd.read_csv('marc_data.csv')
dataframe.columns = ['m007', 'm245']
dataframe['m245'] = dataframe['m245'].map(lambda title: f'$a{title}.' )
dataframe['m245_indicators'] = '10'
```

Our dataframe now looks like this:

| m007 | m245                               |
| ---- | ---------------------------------- |
| ta   | $aWoman in the nineteenth century. |
| ta   | $aThe fire next time.              |

To convert the dataframe into a series of MARC records, we load it into an instance of pandas-marc's `MARCDataFrame` class. This allows us to generate pymarc `Record` objects from the dataframe rows:

```python
from pandas_marc import MARCDataFrame

mdf = MARCDataFrame(dataframe)

for record in mdf.records:
    print(record.title())
```

Output:

```
Woman in the nineteenth century.
The fire next time.
```

`Record` objects may be readily serialized using pymarc's `MARCWriter` class:

```python
from pymarc import MARCWriter

with open('marc_data.mrc', 'wb') as marc_file:
    writer = MARCWriter(marc_file)
    for record in mdf.records:
        writer.write(record)
```

### Indicators



### Delimiters

pandas-marc uses the following delimiters by default:

* **Subfields** are delimited with a dollar sign, `$`. For example, here is a [MARC 100] personal name field comprising an author name and relator term under subfields `a` and `e`: `$aZitkála-Šá, $eauthor.`
* **Multiple field occurrences** may be delimited with a backslash, `\`. For example, here is a series of delimited [MARC 650] subject fields: `$aRhetoric.\$aSpeeches.`

Alternate delimiters can be specified using arguments to `MARCDataFrame`:

```python
mdf = MARCDataFrame(
    dataframe=dataframe,
    occurrence_delimiter='|',
    subfield_delimiter='‡'
)
```

[MARC 100]: https://www.oclc.org/bibformats/en/1xx/100.html
[MARC 650]: https://www.oclc.org/bibformats/en/6xx/650.html

### Installation

Download the latest stable release from the master branch and install with pip:

```sh
pip install pandas-marc.tar.gz
```

### Tests

Run pandas-marc's test suite using [pytest]:

```sh
pytest tests/test_pandas_marc.py

# Or just...
pytest
```
