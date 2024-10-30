import sys
import os

sys.path.append(os.path.abspath(".."))

import polars as pl
import statcast_pitches
from update.schema import STATCAST_SCHEMA


def test_load_all() -> None:
    df = statcast_pitches.load()

    assert isinstance(df, pl.DataFrame)
    assert STATCAST_SCHEMA == df.collect_schema()


def test_load_query() -> None:
    test_query = f"""
        SELECT game_date, bat_speed, swing_length
        FROM pitches
        WHERE
            YEAR(game_date) = '2024'
            AND bat_speed IS NOT NULL;
        """

    df = statcast_pitches.load(query=test_query)

    assert isinstance(df, pl.DataFrame)
    assert len(df.columns) == 3
    assert all(df["bat_speed"].is_not_null())
    assert all(df["swing_length"].is_not_null())
    assert all(df["game_date"].dt.year() == "2024")
