import os
import sys
import io
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter, date2num
import datetime as dt
from itertools import cycle
from doan.util import get_tmp_file_name
from doan.dataset import Dataset


def plot_date(datasets, color='b', ls='', xlabel='', ylabel='', title='',
              output=None):
    if isinstance(datasets, Dataset):
        datasets = [datasets]

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    try:
        del colors[colors.index(color)]
        colors.insert(0, color)
    except IndexError:
        pass
    colors = cycle(colors)

    fig, ax = plt.subplots()
    # TODO auto formatter
    ax.xaxis.set_major_locator(HourLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%H'))
    # ax.xaxis.set_minor_locator(MinuteLocator())
    ax.autoscale_view()
    ax.fmt_xdata = DateFormatter('%H:%M')
    ax.grid(True)

    for dataset in datasets:
        dates = date2num(dataset.get_column_by_type(dataset.DATE))
        values = list(dataset.get_column_by_type(dataset.NUM))
        color = next(colors)
        plt.plot_date(dates, values, color=color, ls=ls, label=dataset.name)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.legend(loc='best', prop={'size':10})
    filename = output or get_tmp_file_name('.png')
    plt.savefig(filename)
    return filename


def hist(dataset, output=None, **kwargs):
    values = Dataset.get_num_column_or_list(dataset)
    defaults = {
        'grid': True,
        'xlabel': '',
        'ylabel': '',
        'title': 'Histogram'
    }
    params = {'bins': 20,
              'normed': 1,
              'facecolor': 'green',
              'alpha': 0.75,
    }
    params.update(kwargs)
    defaults.update(kwargs)
    n, bins, patches = plt.hist(values, **params)
    plt.xlabel(defaults['xlabel'])
    plt.ylabel(defaults['ylabel'])
    plt.title(defaults['title'])
    plt.grid(defaults['grid'])

    filename = output or get_tmp_file_name('.png')
    plt.savefig(filename)

    return filename
