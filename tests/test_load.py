import polars as pl
import statcast_pitches
import pytest


STR_QUERY = """
    SELECT game_date, bat_speed, swing_length
    FROM pitches
    WHERE
        YEAR(game_date) =?
        AND bat_speed IS NOT NULL
    LIMIT 10;
"""


@pytest.mark.parametrize("query", (STR_QUERY, "tests/test_data/test.sql"))
def test_load_query(query) -> None:
    params = ("2024",)

    df = statcast_pitches.load(
        query=query,
        params=params,
    )

    assert isinstance(df, pl.LazyFrame)
    assert len(df.collect_schema().names()) == 3

    df = df.collect()
    assert len(df == 10)
    assert all(df["bat_speed"].is_not_null())
    assert all(df["swing_length"].is_not_null())
    assert all(df["game_date"].dt.year() == "2024")
