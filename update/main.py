from huggingface_hub import HfApi
import polars as pl
import pybaseball
import datetime
import os

from utils import LOCAL_STATCAST_DATA_LOC, HF_DATASET_LOC
from schema import STATCAST_SCHEMA


HF_TOKEN = os.environ.get("HF_TOKEN")


def yesterday() -> datetime.date:
    return datetime.datetime.now().date() - datetime.timedelta(days=1)


def update_statcast(date: datetime.date) -> pl.DataFrame:
    """Updates the statcast DataFrame with data from last date, to the date argument"""
    old_df = pl.read_parquet(HF_DATASET_LOC)
    latest_date = old_df["game_date"].sort(descending=True)[0].date()
    if latest_date == date:
        print("No Updates Needed")
        old_df.write_parquet(LOCAL_STATCAST_DATA_LOC)
        return old_df

    new_df = pl.from_pandas(
        pybaseball.statcast(
            start_dt=latest_date.strftime("%Y-%m-%d"),
            end_dt=date.strftime("%Y-%m-%d"),
        ),
        schema_overrides=STATCAST_SCHEMA,
    ).with_columns(pl.col("game_date").cast(pl.Datetime("us")).alias("game_date"))

    updated_df = pl.concat([old_df, new_df])
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
    _ = update_statcast(date=yesterday())
    _ = upload_to_hf()
