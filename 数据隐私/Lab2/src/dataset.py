import numpy as np
import pandas as pd


class Dataset:
    def __init__(self, has_label, raw_dataset, header):
        self._header = header
        self.has_label = has_label

        self.set_dataset(raw_dataset)

    @classmethod
    def from_csv(cls, *, has_label, abs_path, has_header=False):
        header_arg = 0 if has_header else None
        df_dataset = pd.read_csv(abs_path, header=header_arg, skipinitialspace=True)
        np_dataset = df_dataset.to_numpy()

        if has_header:
            header = df_dataset.columns.values.tolist()
        else:
            offset = 2 if has_label else 1
            n_feats = np_dataset.shape[1] - offset
            header = cls._gen_header(has_label, n_feats)

        return cls(
            has_label=has_label,
            raw_dataset=np_dataset,
            header=header,
        )

    @property
    def features(self):
        if not hasattr(self, "_features"):
            if self.has_label:
                setattr(self, "_features", self._raw_dataset[:, 2:])
            else:
                setattr(self, "_features", self._raw_dataset[:, 1:])
        return getattr(self, "_features")

    @property
    def labels(self):  # read only
        if not self.has_label:
            raise AttributeError("Passive party has no labels.")

        if not hasattr(self, "_labels"):
            raw_labels = self._raw_dataset[:, 1]
            raw_labels = raw_labels.astype(np.int32)
            setattr(self, "_labels", raw_labels)
        return getattr(self, "_labels")

    @property
    def n_features(self):  # read only
        return self.features.shape[1]

    @property
    def n_samples(self):  # read only
        return self.features.shape[0]

    def set_dataset(self, new_raw_dataset) -> None:
        # must delete old properties to save memory
        if hasattr(self, "_raw_dataset"):
            del self._raw_dataset
        if hasattr(self, "_ids"):
            del self._ids
        if hasattr(self, "_features"):
            del self._features
        if hasattr(self, "_labels"):
            del self._labels

        # update new property
        self._raw_dataset = new_raw_dataset

    def get_dataset(self):
        return self._raw_dataset

    @staticmethod
    def _gen_header(has_label, n_feats):
        feats_header = ["x{}".format(i) for i in range(n_feats)]
        if has_label:
            header = ["id"] + ["y"] + feats_header
        else:
            header = ["id"] + feats_header

        return header
