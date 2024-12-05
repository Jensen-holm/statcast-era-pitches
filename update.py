from huggingface_hub import HfApi
from typing import Optional
import polars as pl
import pybaseball
import datetime
import os

from update.utils import LOCAL_STATCAST_DATA_LOC, HF_DATASET_LOC
from update.schema import STATCAST_SCHEMA


HF_TOKEN = os.environ.get("HF_TOKEN")


def yesterday() -> datetime.date:
    return datetime.datetime.now().date() - datetime.timedelta(days=1)


def refresh_statcast() -> pl.DataFrame:
    """Completley refreshed the hugging face dataset"""
    new_df = pl.from_pandas(
        pybaseball.statcast(
            start_dt="2015-04-05",
            end_dt=yesterday().isoformat(),
        ),
        schema_overrides=STATCAST_SCHEMA,
    ).with_columns(pl.col("game_date").cast(pl.Datetime("us")).alias("game_date"))

    new_df.write_parquet(LOCAL_STATCAST_DATA_LOC)
    return new_df


def update_statcast(
    date: datetime.date, refresh: bool = False
) -> Optional[pl.DataFrame]:
    """Updates the statcast DataFrame with data from last date, to the date argument"""
    if refresh:
        return refresh_statcast()

    old_df = pl.scan_parquet(HF_DATASET_LOC)
    latest_date = (
        old_df.select("game_date")
        .sort(by="game_date", descending=True)
        .slice(0, 1)
        .collect()
        .item()
        .date()
    )

    if latest_date == date or date.month in {12, 1, 2}:
        return print(f"No updates needed for {date}")

    new_df = pl.from_pandas(
        pybaseball.statcast(
            start_dt=latest_date.strftime("%Y-%m-%d"),
            end_dt=date.strftime("%Y-%m-%d"),
        ),
        schema_overrides=STATCAST_SCHEMA,
    ).with_columns(pl.col("game_date").cast(pl.Datetime("us")).alias("game_date"))

    updated_df = pl.concat([old_df.collect(), new_df], how="diagonal_relaxed")
    updated_df.write_parquet(LOCAL_STATCAST_DATA_LOC)

    print(f"Saved New Statcast Data from {latest_date} to {date}")
    return updated_df


def upload_to_hf() -> None:
    api = HfApi(token=HF_TOKEN)
    api.upload_file(
        path_or_fileobj=LOCAL_STATCAST_DATA_LOC,
        path_in_repo="data/statcast_era_pitches.parquet",
        repo_id="Jensen-holm/statcast-era-pitches",
        repo_type="dataset",
    )


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument(
        "-refresh",
        type=bool,
        default=False,
        help="whether or not to refresh the data base by reloading all statcast data",
    )

    parser.add_argument(
        "-date",
        type=datetime.date.fromisoformat,
        default=yesterday(),
        help="if refresh is false, then this program will check for new data up to this date",
    )

    if update_statcast(**parser.parse_args().__dict__) is not None:
        _ = upload_to_hf()
