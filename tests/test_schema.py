import polars as pl
import statcast_pitches
from update.schema import STATCAST_SCHEMA
import pytest


def _default_pl_lf() -> pl.LazyFrame:
    return statcast_pitches.load()


def _sql_lf() -> pl.LazyFrame:
    params = ("2024",)
    test_query = """
        SELECT *
        FROM pitches
        WHERE
            YEAR(game_date) =?
            AND bat_speed IS NOT NULL
        LIMIT 10;
    """

    return statcast_pitches.load(
        query=test_query,
        params=params,
    )


@pytest.mark.parametrize("lf_fn", [_sql_lf, _default_pl_lf])
def test_pl_lazy_schema(lf_fn: pl.LazyFrame) -> None:
    lf = lf_fn()
    assert isinstance(lf, pl.LazyFrame)
    assert STATCAST_SCHEMA == dict(lf.collect_schema())
