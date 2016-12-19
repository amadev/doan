from doan.util import lines
from operator import itemgetter
from subprocess import check_call
from dateutil.parser import parse
from doan.util import get_tmp_file_name


class Dataset(object):

    """Table with determined columns data type.

    Features:
    - Data loading with respect to column type
      (Lines and elements splitting is on iterator side).
    - Columns iterator.
    - Getting column with predifined type.
    """

    DATE = 'd'
    NUM = 'num'
    STRING = 's'
    FLOAT = 'float'
    INT = 'int'

    # TODO types register
    TYPES = {FLOAT: lambda v: float(v),
             INT: lambda v: int(i),
             STRING: lambda v: v,
             DATE: lambda v: parse(v)}

    TYPES_MAP = {NUM: [INT, FLOAT],
                 DATE: [DATE]}

    class ParseError(Exception):
        pass

    def __init__(self, column_types=[FLOAT]):
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

    def get_column_by_type(self, column_type):
        column = list(filter(lambda i: i in self.TYPES_MAP[column_type],
                             self.column_types))
        if len(column) != 1:
            raise ValueError('Can not find single num column')
        return self.column(self.column_types.index(column[0]))

    @staticmethod
    def get_num_column_or_list(dataset):
        if isinstance(dataset, Dataset):
            return dataset.get_column_by_type(Dataset.NUM)
        return dataset


def cmd(command):
    fn = get_tmp_file_name()
    check_call(command + ' > {}'.format(fn), shell=True)
    return fn


def ssh(host):
    def wrapped(command):
        fn = get_tmp_file_name()
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
    dataset = Dataset([Dataset.FLOAT])
    return dataset.load(LinesIterator(obj))


def r_date_num(obj, multiple=False):
    """Read date-value table."""
    if isinstance(obj, (list, tuple)):
        it = iter
    else:
        it = LinesIterator
    if multiple:
        datasets = {}
        for line in it(obj):
            label = line[2]
            if label not in datasets:
                datasets[label] = Dataset([Dataset.DATE, Dataset.FLOAT])
                datasets[label].name = label
            datasets[label].parse_elements(line[0:2])
        return datasets.values()
    dataset = Dataset([Dataset.DATE, Dataset.FLOAT])
    return dataset.load(it(obj))
