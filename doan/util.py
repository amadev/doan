import io


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
