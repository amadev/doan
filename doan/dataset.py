from doan.util import lines
from operator import itemgetter


class Dataset(object):
    types_map = {'num': ['i', 'f']}
    def __init__(self, name):
        self.name = name
        self.rows = []
        column_types = []
        self.length = 0

    def __len__(self):
        return self.length

    def add_row(self, row):
        self.rows.append(row)
        self.length += 1

    def __iter__(self):
        return iter(self.rows)

    def column(self, *args):
        for row in self.rows:
            yield itemgetter(*args)(row)

    def num_column(self):
        column = list(filter(lambda i: i in self.types_map['num'],
                             self.column_types))
        if len(column) != 1:
            raise ValueError('Can not find single num column')
        return self.column(self.column_types.index(column[0]))


def _get_iterator(obj):
    it = obj
    name = 'unknown'
    # assume that string is filename
    if isinstance(obj, str):
        # TODO unclosed file issue
        it = open(obj)
        name = obj
    if hasattr(obj, 'doan_dataset_name'):
        name = obj.doan_dataset_name
    setattr(it, 'doan_dataset_name', name)
    return it


def r_num(obj):
    """Read list of numbers."""
    it = _get_iterator(obj)
    dataset = Dataset(it.doan_dataset_name)
    dataset.column_types = ['f']
    for line in lines(it):
        # TODO move logic to dataset
        dataset.add_row([float(line)])
    return dataset
