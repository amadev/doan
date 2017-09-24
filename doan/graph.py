import os
import sys
import io
import matplotlib
matplotlib.use('AGG')
# TODO use right functions for matplotlib
import matplotlib.pyplot as plt  # noqa
from matplotlib.dates import (  # noqa
    HourLocator, MinuteLocator, DateFormatter, date2num)  # noqa
import matplotlib.mlab as mlab  # noqa
import datetime as dt  # noqa
from itertools import cycle  # noqa
from doan.util import get_tmp_file_name  # noqa
from doan.dataset import Dataset  # noqa
from doan.stat import mean, std  # noqa


def _update_params(defaults, plot_params, new):
    new_plot_params = {}
    for k, v in new.items():
        if k in defaults:
            defaults[k] = v
        else:
            new_plot_params[k] = v
    plot_params.update(new_plot_params)


def plot_date(datasets, **kwargs):
    """Plot points with dates.

    datasets can be Dataset object or list of Dataset.
    """

    defaults = {
        'grid': True,
        'xlabel': '',
        'ylabel': '',
        'title': '',
        'output': None,
        'figsize': (8, 6),
    }
    plot_params = {
        'color': 'b',
        'ls': '',
        'alpha': 0.75,
    }
    _update_params(defaults, plot_params, kwargs)
    if isinstance(datasets, Dataset):
        datasets = [datasets]

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    color = plot_params.pop('color')
    try:
        del colors[colors.index(color)]
        colors.insert(0, color)
    except IndexError:
        pass
    colors = cycle(colors)

    fig, ax = plt.subplots()
    fig.set_size_inches(*defaults['figsize'])
    fig.autofmt_xdate()
    ax.autoscale_view()

    for dataset in datasets:
        if isinstance(dataset, Dataset):
            dates = list(dataset.get_column_by_type(dataset.DATE))
            values = list(dataset.get_column_by_type(dataset.NUM))
            label = dataset.name
        else:
            dates, values = dataset
            label = ''
        dates = date2num(dates)
        color = next(colors)
        plt.plot_date(dates, values, color=color, label=label, **plot_params)

    plt.xlabel(defaults['xlabel'])
    plt.ylabel(defaults['ylabel'])
    plt.title(defaults['title'])
    plt.grid(defaults['grid'])

    plt.legend(loc='best', prop={'size': 10})
    filename = defaults['output'] or get_tmp_file_name('.png')
    plt.savefig(filename)
    return filename


def hist(dataset, **kwargs):
    defaults = {
        'grid': False,
        'xlabel': '',
        'ylabel': '',
        'title': '',
        'output': None,
        'norm_line': True,
        'figsize': (8, 6),
    }
    plot_params = {
        'bins': 20,
        'normed': 1,
        'facecolor': 'green',
        'alpha': 0.75,
    }
    _update_params(defaults, plot_params, kwargs)

    fig, ax = plt.subplots()
    fig.set_size_inches(*defaults['figsize'])

    values = list(Dataset.get_num_column_or_list(dataset))

    n, bins, patches = plt.hist(values, **plot_params)

    if defaults['norm_line']:
        y = mlab.normpdf(bins, mean(values), std(values))
        l = plt.plot(bins, y, 'r--', linewidth=1)

    plt.xlabel(defaults['xlabel'])
    plt.ylabel(defaults['ylabel'])
    plt.title(defaults['title'])
    plt.grid(defaults['grid'])

    filename = defaults['output'] or get_tmp_file_name('.png')
    plt.savefig(filename)

    return filename
