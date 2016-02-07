import uuid
from doan.util import lines
from operator import itemgetter
from subprocess import check_call
from dateutil.parser import parse


class Dataset(object):

    """Table with determined columns data type.

    Features:
    - Data loading with respect to column type
      (Lines and elements splitting is on iterator side).
    - Columns iterator.
    - Getting column with predifined type.
    """

    # TODO types register
    TYPES = {'f': lambda v: float(v),
             'i': lambda v: int(i),
             's': lambda v: v,
             'd': lambda v: parse(v)}

    TYPES_MAP = {'num': ['i', 'f']}

    class ParseError(Exception):
        pass

    def __init__(self, column_types=['f']):
        self.name = ''
        self.rows = []
        # TODO parse column types
        self.column_types = column_types
        self.length = 0

    def __len__(self):
        return self.length

    def load(self, iterator):
        if hasattr(iterator, 'name'):
            self.name = iterator.name
        for i, elements in enumerate(iterator):
            self.line_index = i + 1
            self.parse_elements(elements)
        return self

    def parse_elements(self, elements):
        row = [self.parse_value(v, i) for i, v in enumerate(elements)]
        self.add_row(row)

    def parse_value(self, val, type_index):
        try:
            return self.TYPES[self.column_types[type_index]](val)
        except ValueError:
            raise self.ParseError(
                ('Invalid value "{}" '
                 'in line {} for "{}" column type (index: {})').format(
                     val, self.line_index, self.column_types[type_index],
                     type_index))

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


def _tmp_file(ext=''):
    return '/tmp/doan-{}{}'.format(uuid.uuid4(), ext)


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
    """Iterate file or any iterable object.

    Object knows how to split lines and elements.
    """
    # TODO move util.lines here
    def __init__(self, obj):
        self.obj = obj
        self.is_file = isinstance(obj, str)
        self.name = 'iterator' if not self.is_file else obj

    def __iter__(self):
        if self.is_file:
            with open(self.obj) as it:
                for i in lines(it):
                    yield self.split_line(i)
        else:
            for i in lines(self.obj):
                yield self.split_line(i)

    def split_line(self, line):
        return line.split()


def r_num(obj):
    """Read list of numbers."""
    dataset = Dataset(['f'])
    return dataset.load(LinesIterator(obj))


def r_date_num(obj):
    """Read date-value table."""
    dataset = Dataset(['d', 'f'])
    return dataset.load(LinesIterator(obj))
