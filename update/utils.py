from huggingface_hub.hf_api import HfApi
from enum import Enum
import datetime
import os

__all__ = [
    "LOCAL_STATCAST_DATA_LOC",
    "HF_DATASET_LOC",
    "UpdateFlag",
    "yesterday",
    "upload_to_hf",
]

LOCAL_STATCAST_DATA_LOC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "statcast_era_pitches.parquet",
)

HF_DATASET_LOC = (
    "hf://datasets/Jensen-holm/statcast-era-pitches/data/statcast_era_pitches.parquet"
)


class UpdateFlag(Enum):
    COMPLETE = 0
    NOT_NEEDED = 1
    ERROR = 2


def yesterday() -> datetime.date:
    return datetime.datetime.now().date() - datetime.timedelta(days=1)


def upload_to_hf(hf_tok: str) -> None:
    api = HfApi(token=hf_tok)
    api.upload_file(
        path_or_fileobj=LOCAL_STATCAST_DATA_LOC,
        path_in_repo="data/statcast_era_pitches.parquet",
        repo_id="Jensen-holm/statcast-era-pitches",
        repo_type="dataset",
    )
