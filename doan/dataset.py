import uuid
from doan.util import lines
from operator import itemgetter
from subprocess import check_call


class Dataset(object):

    """Table with determined columns data type.

    Features:
    - Data reading with respect to column type.
    - Columns iterator.
    - Getting column with predifined type.
    """

    TYPES = {'f': lambda v: float(v)}
    TYPES_MAP = {'num': ['i', 'f']}

    def __init__(self, name):
        self.name = ''
        self.rows = []
        column_types = []
        self.length = 0

    def __len__(self):
        return self.length

    def parse_line(self, line):
        row = [self.parse_value(v, i) for i, v in enumerate(line.split())]
        self.add_row(row)

    def parse_value(self, v, i):
        return self.TYPES[self.column_types[i]](v)

    def add_row(self, row):
        self.rows.append(row)
        self.length += 1

    def __iter__(self):
        return iter(self.rows)

    def column(self, *args):
        for row in self.rows:
            yield itemgetter(*args)(row)

    def num_column(self):
        column = list(filter(lambda i: i in self.TYPES_MAP['num'],
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


def _tmp_file():
    return '/tmp/doan-{}'.format(uuid.uuid4())


def cmd(command):
    fn = _tmp_file()
    check_call(command + ' > {}'.format(fn), shell=True)
    return fn


def ssh(host):
    def wrapped(command):
        fn = _tmp_file()
        check_call('ssh {} "{} > {}"\n'.format(
            host, command.replace(r'"', r'\"').replace('$', r'\$'), fn),
                   shell=True)
        check_call('scp {0}:{1} {1}'.format(host, fn),
                   shell=True)
        return fn
    return wrapped


class LinesIterator:
    """Iterate file or any iterable object. """

    def __init__(self, obj):
        self.obj = obj
        self.is_file = isinstance(obj, str)
        self.name = 'iterator' if not self.is_file else obj

    def __iter__(self):
        if self.is_file:
            with open(self.obj) as it:
                for i in lines(it):
                    yield i
        else:
            for i in lines(self.obj):
                yield i


def r_num(obj):
    """Read list of numbers."""
    dataset = Dataset('test')
    dataset.column_types = ['f']
    it = LinesIterator(obj)
    if it.name:
        dataset.name = it.name

    for line in it:
        dataset.parse_line(line)

    return dataset


# def r_dvn(obj):
#     """Read date-value-name table."""
#     pass
