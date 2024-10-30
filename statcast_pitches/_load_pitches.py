from typing import TypeAlias, Optional, Tuple

import polars as pl
import pandas as pd
import duckdb

from ._utils import *

__all__ = ["load"]

DataLike: TypeAlias = pd.DataFrame | pl.DataFrame


def _load_all_polars() -> pl.DataFrame:
    """Load the entire dataset using polars."""
    return pl.read_parquet(HF_DATASET_LOC)


def _load_all_pandas() -> pd.DataFrame:
    """Load the entire dataset using pandas."""
    return pd.read_parquet(HF_DATASET_LOC)


def load(
    query: Optional[str] = None, params: Optional[Tuple] = None, pandas: bool = False
) -> DataLike:
    """
    Returns a DataFrame object (either polars or pandas) containing statcast pitch data

    Arguments
    ---------
    pandas : bool
        set to True if you want to return the output as a pandas DataFrame, leave as
        False to get a polars DataFrame.

    query : Optional[str]
        optional duckdb SQL query to execute before loading data. The name of the table is
        registered as 'pitches'. This is suggested when you don't want to download all
        7M+ rows (575mb). query is None by default, meaning if it is not specified you will
        download all of the pitches.

        example :
            import statcast_pitches

            params = ("2024",)
            query = f'''
                SELECT bat_speed, swing_length
                FROM pitches
                WHERE YEAR(game_date) =?
                    AND bat_speed IS NOT NULL;
            '''

            swing_data_24_df = statcast_pitches.load(
                query=query,
                params=params,
            )

    params : Tuple
        if you specify a query, and your query is expecting parameters, this is where you put them.
    """
    if query is None:
        return _load_all_polars() if not pandas else _load_all_pandas()

    with duckdb.connect() as con:
        _ = con.execute(INSTALL_DB_REQS_QUERY)
        _ = con.execute(REGISTER_QUERY)
        result = con.sql(query=query, params=params)
        return result.pl() if not pandas else result.df()
