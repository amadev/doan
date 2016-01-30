def mean(dataset):
    data = dataset.num_column()
    return sum(data) / float(len(dataset))
