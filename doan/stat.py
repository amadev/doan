import math

def mean(dataset):
    data = dataset.num_column()
    return sum(data) / float(len(dataset))

def std(dataset, m=None):
    n = len(dataset)
    values = dataset.num_column()
    if m is None:
        m = mean(dataset)
    return (sum((i - m) ** 2  for i in values) / float(n)) ** 0.5


class stat():
    def __init__(self, dataset):
        self.mean = mean(dataset)
        self.std = std(dataset, self.mean)
        self.percentiles = percentiles(dataset, [0.05, 0.16, 0.25, 0.5, 0.75, 0.84, 0.95])
        self.calced_percentiles = [
            self.mean - 2 * self.std,
            self.mean - self.std,
            self.mean - 0.67 * self.std,
            self.mean,
            self.mean + 0.67 * self.std,
            self.mean + self.std,
            self.mean + 2 * self.std]
        self.max = max(dataset.num_column())
        self.min = min(dataset.num_column())

    def __repr__(self):
        return '{}'.format(self.__dict__)

    # TODO pretty print stat format

    # def __str__(self):
    #     return '|{}|{}|'.format(fixed_text('Mean', 15), fixed_float(self.mean, 14,6))


def _percentile(values, n, percentile):
    ind = (n - 1) * percentile
    d, u = math.floor(ind), math.ceil(ind)
    if d == u:
        return values[d]
    else:
        return (values[d] + values[u]) / 2.


def percentiles(dataset, vals):
    n = len(dataset)
    values = list(dataset.num_column())
    values.sort()
    return [_percentile(values, n, p) for p in vals]
