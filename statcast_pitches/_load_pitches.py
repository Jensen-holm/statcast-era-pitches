from typing import TypeAlias, Optional

import polars as pl
import pandas as pd
import duckdb

from ._utils import HF_DATASET_LOC

__all__ = ["load"]

DataLike: TypeAlias = pd.DataFrame | pl.DataFrame


def _load_all_polars() -> pl.DataFrame:
    """Load the entire dataset using polars."""
    return pl.read_parquet(HF_DATASET_LOC)


def _load_all_pandas() -> pd.DataFrame:
    """Load the entire dataset using pandas."""
    return pd.read_parquet(HF_DATASET_LOC)


def load(query: Optional[str] = None, pandas: bool = False) -> DataLike:
    """
    Returns a DataFrame object (either polars or pandas) containing statcast pitch data

    Arguments
    ---------
    pandas : bool
        set to True if you want to return the output as a pandas DataFrame, leave as
        False to get a polars DataFrame.

    query : Optional[str]
        optional duckdb SQL query to execute before loading data. This is suggested
        when you don't want to download all 7M+ rows (575mb). query is None by default,
        meaning if it is not specified you will download all of the pitches.
    """
    if query is None:
        return _load_all_polars() if not pandas else _load_all_pandas()

    with duckdb.connect(database=HF_DATASET_LOC) as con:
        result = con.sql(query=query)
        return result.pl() if not pandas else result.df()
