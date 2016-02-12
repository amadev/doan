import math
from doan.util import fixed_width, num_list_equal
from doan.dataset import Dataset


PERCENTILES = [0.05, 0.16, 0.25, 0.5, 0.75, 0.84, 0.95]


def mean(dataset):
    values = Dataset.get_num_column_or_list(dataset)
    return sum(values) / float(len(dataset))


def std(dataset, m=None):
    n = len(dataset)
    values = Dataset.get_num_column_or_list(dataset)
    if m is None:
        m = mean(dataset)
    return (sum((i - m) ** 2  for i in values) / float(n)) ** 0.5


class stat():
    def __init__(self, dataset):
        self.mean = mean(dataset)
        self.std = std(dataset, self.mean)
        self.percentiles = percentiles(dataset,  PERCENTILES)
        self.calculated_percentiles = [
            self.mean - 2 * self.std,
            self.mean - self.std,
            self.mean - 0.67 * self.std,
            self.mean,
            self.mean + 0.67 * self.std,
            self.mean + self.std,
            self.mean + 2 * self.std]
        self.max = max(Dataset.get_num_column_or_list(dataset))
        self.min = min(Dataset.get_num_column_or_list(dataset))
        self.is_normal = self._is_normal(
            self.percentiles, self.calculated_percentiles)
        self.length = len(dataset)

    def __repr__(self):
        return '{}'.format(self.__dict__)

    def __str__(self):
        def fw(s):
            return fixed_width(s, 15)
        def tb(*args):
            return '|{}|\n'.format('|'.join([fw(i) for i in args]))
        return (tb('length', self.length) +
                tb('mean', self.mean) +
                tb('std', self.std) +
                tb('max', self.max) +
                tb('min', self.min) +
                tb('', *['{:.0f}%'.format(i * 100) for i in PERCENTILES]) +
                tb('pcs.', *self.percentiles) +
                tb('calc. pcs.', *self.calculated_percentiles) +
                tb('normality', self.is_normal))

    def _is_normal(self, prs, calc_prs):
        return num_list_equal(prs, calc_prs, 0.05)


def _percentile(values, n, percentile):
    ind = (n - 1) * percentile
    d, u = math.floor(ind), math.ceil(ind)
    if d == u:
        return values[d]
    else:
        return (values[d] + values[u]) / 2.


def percentiles(dataset, vals):
    n = len(dataset)
    values = list(Dataset.get_num_column_or_list(dataset))
    values.sort()
    return [_percentile(values, n, p) for p in vals]
