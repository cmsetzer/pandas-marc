"""A library for working with MARC metadata using pandas dataframes."""

from itertools import chain

from pymarc import Field, Record

OCCURRENCE_DELIMITER = '\\'
SUBFIELD_DELIMITER = '$'


class MARCDataFrame(object):
    """A class for converting a dataframe to a sequence of MARC records.

    Given a dataframe with column headings of the form 'm001', 'm245',
    etc., will generate a series of pymarc MARC record objects with their
    associated fields.
    """
    def __init__(self, dataframe, occurrence_delimiter=OCCURRENCE_DELIMITER,
                 subfield_delimiter=SUBFIELD_DELIMITER):
        self.dataframe = dataframe
        self.occurrence_delimiter = occurrence_delimiter
        self.subfield_delimiter = subfield_delimiter

    def generate_subfields(self, occurrence):
        """Split a field value into subfield codes and subfield values.

        If the value does not begin with a subfield delimiter and code,
        the first subfield is presumed to be subfield 'a'.
        """
        if not occurrence.startswith(self.subfield_delimiter):
            occurrence = 'a{}'.format(occurrence)
        for subfield in occurrence.split(self.subfield_delimiter):
            try:
                code, *value = subfield
            except ValueError:
                continue
            else:
                if value:
                    yield code, ''.join(value)

    def generate_fields(self, row):
        """Construct fields for each row and yield them in turn.

        Values containing the instance's supplied occurrence delimiter
        will be split up on the assumption that they represent multiple
        occurrences of a MARC field (e.g., multiple MARC 650s).
        """
        for key, value in row.items():
            # key examples: leader, m008, m245, m245_indicators
            if key == 'leader' or key.endswith('_indicators'):
                continue
            # tag examples: 008, 245
            tag = key[1:]
            # Special logic for control fields
            if tag in ['001', '003', '005', '006', '007', '008', '009']:
                yield Field(tag, data=value)
                continue
            indicators = tuple(row['{}_indicators'.format(key)])
            # Split field occurrences on delimiter and delegate to another
            # generator for subfield codes and values
            occurrences = value.split(self.occurrence_delimiter)
            for occurrence in occurrences:
                subfields = list(chain(*self.generate_subfields(occurrence)))
                yield Field(tag, indicators, subfields)

    def generate_records(self):
        """Iterate over the dataframe and yield a record for each row.

        If the dataframe includes a series (column) with the name
        'leader', that series's value will be used to construct the
        record leader for each row. Otherwise, pymarc's default leader
        value will be used instead.
        """
        for _, row in self.dataframe.iterrows():
            record = Record()
            try:
                if row['leader']:
                    record.leader = row['leader']
            except KeyError:
                pass
            for field in self.generate_fields(row):
                record.add_field(field)
            yield record

    @property
    def records(self):
        """Get a generator of MARC records from the dataframe."""
        return self.generate_records()
