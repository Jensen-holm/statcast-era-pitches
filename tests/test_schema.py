import polars as pl
import statcast_pitches
from update.schema import STATCAST_SCHEMA


def test_lazy_schema() -> None:
    df = statcast_pitches.load()

    assert isinstance(df, pl.LazyFrame)
    assert STATCAST_SCHEMA == dict(df.collect_schema())
