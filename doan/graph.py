import os
import sys
import io
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter, date2num
import datetime as dt
from itertools import cycle
from doan.util import get_tmp_file_name
from doan.dataset import Dataset


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
    }
    graph_params = {
        'color': 'b',
        'ls': '',
        'alpha': 0.75,
    }
    graph_params.update(kwargs)
    [plot_params.pop(k) for k in defaults if k in plot_params]
    defaults.update(kwargs)

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
    #ax.fmt_xdata = DateFormatter("%H:%M")
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

    plt.legend(loc='best', prop={'size':10})
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
    }
    plot_params = {
        'bins': 20,
        'normed': 1,
        'facecolor': 'green',
        'alpha': 0.75,
    }
    plot_params.update(kwargs)
    [plot_params.pop(k) for k in defaults if k in plot_params]
    defaults.update(kwargs)

    values = list(Dataset.get_num_column_or_list(dataset))

    n, bins, patches = plt.hist(values, **plot_params)
    plt.xlabel(defaults['xlabel'])
    plt.ylabel(defaults['ylabel'])
    plt.title(defaults['title'])
    plt.grid(defaults['grid'])

    filename = defaults['output'] or get_tmp_file_name('.png')
    plt.savefig(filename)

    return filename
