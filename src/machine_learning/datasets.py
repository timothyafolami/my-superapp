from sklearn import datasets
from sklearn.model_selection import train_test_split
import typing as t
import streamlit as st
import pandas as pd


class DatasetParams(t.TypedDict):
    source: t.Literal["iris", "digits", "breast_cancer"]
    test_size: float | None
    shuffle: bool
    stratify: bool


class Dataset:
    def __init__(self, type: t.Literal["classification", "regression"]):
        self.type = type
        self.X: t.Tuple[pd.DataFrame, pd.DataFrame] | None = None
        self.y: t.Tuple[pd.Series, pd.Series] | None = None
        self.label_mapping: t.Dict[int, str] | None = None
        self.descr: str | None = None

    @property
    def params(self) -> t.Dict[str, t.Any]:
        columns = st.columns(3)
        return {
            "source": columns[0].selectbox(
                label="source",
                options=["iris", "digits", "breast_cancer"],
                help="The scikit-learn toy dataset to use.",
            ),
            "test_size": columns[1].slider(
                "test_size",
                min_value=0.05,
                max_value=0.5,
                value=0.2,
                step=0.05,
                help="The proportion of the dataset to include in the test split",
            ),
            "shuffle": columns[2].checkbox(
                label="shuffle",
                value=True,
                help="Whether to shuffle the dataset or not.",
            ),
            "stratify": columns[2].checkbox(
                label="stratify",
                value=False,
                help="Whether to stratify the dataset or not. "
                "Stratifying means keeping the same target distribution in the initial, train and test datasets.",
            ),
        }

    @classmethod
    @st.cache_data(show_spinner=False)
    def get_dataset(_cls, **params: t.Unpack[DatasetParams]) -> t.Dict[str, t.Any]:
        raw_dataset = getattr(datasets, f"load_{params['source']}")(as_frame=True)
        X, y = raw_dataset.data, raw_dataset.target
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=params["test_size"],
            shuffle=params["shuffle"],
            stratify=y if params["stratify"] else None,
            random_state=0,
        )
        return {
            "X": (X_train, X_test),
            "y": (y_train, y_test),
            "label_mapping": dict(enumerate(raw_dataset.target_names)),
            "description": raw_dataset.DESCR,
        }

    def set(self, raw_dataset_dict: t.Dict[str, t.Any]):
        self.X = raw_dataset_dict["X"]
        self.y = raw_dataset_dict["y"]
        self.label_mapping = raw_dataset_dict["label_mapping"]
        self.description = raw_dataset_dict["description"]