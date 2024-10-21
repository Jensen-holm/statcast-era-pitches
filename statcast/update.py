import polars as pl
import pybaseball
import datetime
import warnings
import os

# pybaseball has some pandas future warnings that get annoying
warnings.simplefilter("ignore", FutureWarning)

from .schema import STATCAST_SCHEMA

__all__ = ["update_statcast"]


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATCAST_PARQUET_LOC = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "data", "updated_statcast_pitches.parquet")
)


def update_statcast(date: datetime.date) -> pl.DataFrame:
    """Updates the statcast DataFrame with data from last date, to the date argument"""
    old_df = pl.read_parquet(STATCAST_PARQUET_LOC)
    latest_date = old_df["game_date"].sort(descending=True)[0].date()
    if latest_date == date:
        print("No Updates Needed")
        return old_df

    new_df = pl.from_pandas(
        pybaseball.statcast(
            start_dt=latest_date.strftime("%Y-%m-%d"),
            end_dt=date.strftime("%Y-%m-%d"),
        ),
        schema_overrides=STATCAST_SCHEMA,
    )

    # make sure that the old and new data have the same game_date precision
    new_df = new_df.with_columns(pl.col("game_date").cast(pl.Datetime("us")))
    old_df = old_df.with_columns(pl.col("game_date").cast(pl.Datetime("us")))

    updated_df = pl.concat([old_df, new_df])
    updated_df.write_parquet(STATCAST_PARQUET_LOC)

    print(f"Saved New Statcast Data from {latest_date} to {date}")
    return updated_df
