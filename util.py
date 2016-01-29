import io


def lines(lns):
    for line in lns:
        line = line.strip()
        if not line:
            continue
        yield line
