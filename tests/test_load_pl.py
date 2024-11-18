import sys
import os

sys.path.append(os.path.abspath(".."))

import polars as pl
import statcast_pitches
from update.schema import STATCAST_SCHEMA


def test_load_all_eager() -> None:
    df = statcast_pitches.load()

    assert isinstance(df, pl.LazyFrame)
    assert STATCAST_SCHEMA == df.collect_schema()


def test_load_query() -> None:
    params = ("2024",)
    test_query = f"""
        SELECT game_date, bat_speed, swing_length
        FROM pitches
        WHERE
            YEAR(game_date) =?
            AND bat_speed IS NOT NULL;
    """

    df = statcast_pitches.load(
        query=test_query,
        params=params,
    )

    assert isinstance(df, pl.LazyFrame)
    assert len(df.collect_schema().names()) == 3

    df = df.collect()
    assert all(df["bat_speed"].is_not_null())
    assert all(df["swing_length"].is_not_null())
    assert all(df["game_date"].dt.year() == "2024")
