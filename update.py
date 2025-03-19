import polars as pl
import pybaseball
import datetime
import logging
import os

from update.schema import STATCAST_SCHEMA
from update.utils import (
    LOCAL_STATCAST_DATA_LOC,
    HF_DATASET_LOC,
    UpdateFlag,
    upload_to_hf,
    yesterday,
)

# pybaesball has some pandas code that generates some warnings.
# why should I pay for the sins of pybaseball?
import warnings

warnings.filterwarnings("ignore")


def update_statcast(date: datetime.date) -> UpdateFlag:
    """Updates the statcast DataFrame with data from last date, to the date argument"""
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
        logging.log(logging.INFO, f"no updates needed for {date}")
        return UpdateFlag.NOT_NEEDED

    try:
        new_df = pl.from_pandas(
            pybaseball.statcast(
                start_dt=latest_date.strftime("%Y-%m-%d"),
                end_dt=date.strftime("%Y-%m-%d"),
            ),
            schema_overrides=STATCAST_SCHEMA,
        ).with_columns(pl.col("game_date").cast(pl.Date).alias("game_date"))

        updated_df = pl.concat([old_df.collect(), new_df], how="diagonal_relaxed")
        updated_df.write_parquet(LOCAL_STATCAST_DATA_LOC)
    except Exception as e:
        logging.log(
            logging.INFO,
            f"dataset update failed with the exception {e.__class__}:\n\t{e}",
        )
        return UpdateFlag.ERROR

    logging.log(logging.INFO, f"saved new statcast data from {latest_date} to {date}")
    return UpdateFlag.COMPLETE


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument(
        "-date",
        type=datetime.date.fromisoformat,
        default=yesterday(),
        help="check for new data up to this date",
    )

    if (r := update_statcast(**parser.parse_args().__dict__)) == UpdateFlag.COMPLETE:
        hf_tok = os.environ.get("HF_TOKEN")
        assert hf_tok is not None, f"bad huggingface token |{hf_tok}|"
        _ = upload_to_hf(hf_tok)
