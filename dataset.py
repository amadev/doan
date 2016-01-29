from doan.util import lines


class Dataset(object):
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


def _get_iterator(obj):
    it = obj
    name = 'iterator'
    # assume that string is filename
    if isinstance(obj, str):
        it = open(obj)
        name = obj
    if hasattr(obj, 'doan_dataset_name'):
        name = obj.doan_dataset_name
    setattr(it, 'doan_dataset_name', name)
    return it


def r_num(obj):
    it = _get_iterator(obj)
    d = Dataset(it.doan_dataset_name)
    d.column_types = ['f']
    for line in lines(it):
        d.add_row(float(line))
    return d
