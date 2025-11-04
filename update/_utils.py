from enum import Enum
import datetime
import os

__all__ = [
    "LOCAL_STATCAST_DATA_LOC",
    "DATASET_LOC",
    "UpdateFlag",
    "yesterday",
]

LOCAL_STATCAST_DATA_LOC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "statcast_era_pitches.parquet",
)

DATASET_LOC = (
    # "hf://datasets/Jensen-holm/statcast-era-pitches/data/statcast_era_pitches.parquet"
    "https://raw.githubusercontent.com/Jensen-holm/statcast-era-pitches/main/data/statcast_era_pitches.parquet"
)


class UpdateFlag(Enum):
    COMPLETE = 0
    NOT_NEEDED = 1
    ERROR = 2


def yesterday() -> datetime.date:
    return datetime.datetime.now().date() - datetime.timedelta(days=1)
