from typing import Optional, Tuple

import polars as pl
import duckdb

from ._utils import (
    HF_DATASET_LOC,
    INSTALL_DB_REQS_QUERY,
    REGISTER_QUERY,
)

__all__ = ["load"]


def load(query: Optional[str] = None, params: Optional[Tuple] = None) -> pl.LazyFrame:
    """
    Returns a polars LazyFrame object

    Arguments
    ---------
    params : Optional[Tuple]
        if you specify a query, and your query is expecting parameters, this is where you put them.

    query : Optional[str]
        optional duckdb SQL query to execute before loading data. The name of the table is
        registered as 'pitches'. This is suggested when you don't want to download all
        7M+ rows (575mb). query is None by default, meaning if it is not specified you will
        download all of the pitches.

    example 1 (load all data) :
        import statcast_pitches

        df: pl.LazyFrame = statcast_pitches.load()

    example 2 (query specific pitches) :
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
    """
    if query is None:
        return pl.scan_parquet(HF_DATASET_LOC)

    with duckdb.connect() as con:
        _ = con.execute(INSTALL_DB_REQS_QUERY)
        _ = con.execute(REGISTER_QUERY)
        result = con.sql(query=query, params=params)
        return result.pl().lazy()
