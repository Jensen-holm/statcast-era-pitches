import statcast_pitches
import polars as pl

def test_load_query() -> None:
    params = ("2024",)
    test_query = """
        SELECT game_date, bat_speed, swing_length
        FROM pitches
        WHERE
            YEAR(game_date) =?
            AND bat_speed IS NOT NULL
        LIMIT 10;
    """

    df = statcast_pitches.load(
        query=test_query,
        params=params,
    )

    assert isinstance(df, pl.LazyFrame)
    assert len(df.collect_schema().names()) == 3

    df = df.collect()
    assert len(df) == 10
    assert all(df["bat_speed"].is_not_null())
    assert all(df["swing_length"].is_not_null())
    assert all(df["game_date"].dt.year() == "2024")
