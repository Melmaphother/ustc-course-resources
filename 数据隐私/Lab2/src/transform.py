from sklearn import preprocessing


def scale(dataset):
    raw_dataset = dataset.get_dataset()

    start_col = 2 if dataset.has_label else 1
    scaled_feats = preprocessing.scale(raw_dataset[:, start_col:], copy=False)
    raw_dataset[:, start_col:] = scaled_feats

    dataset.set_dataset(raw_dataset)
