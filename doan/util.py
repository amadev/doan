import io
import logging


def lines(lns):
    for line in lns:
        line = line.strip()
        if not line:
            continue
        yield line


def chunk(seq, n):
    # http://stackoverflow.com/a/312464/190597 (Ned Batchelder)
    """ Yield successive n-sized chunks from seq."""
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def fixed_width(obj, l):
    if isinstance(obj, str):
        if len(obj) > l:
            obj = obj[:l -1] + '.'
        return ('{: >' + str(l) + '}').format(obj)
    elif isinstance(obj, (float, bool)):
        precision = 6
        if l <= precision:
            logging.error('Length is too small for float fixed width, '
                          'use more than {}'.format(precision))
            raise ValueError('Invalid length for float')
        fmt = '{}.{}g'.format(l, precision)
        return ('{:' + fmt + '}').format(obj)
    raise ValueError('There is no fixed width formatting for {}'.format(type(obj)))


def element_equal(v1, v2, precision):
    return abs(v1 - v2) <= v1 * precision


def num_list_equal(l1, l2, precision):
    return all(
        element_equal(v1, l2[i], precision)
        for i, v1 in enumerate(l1))
