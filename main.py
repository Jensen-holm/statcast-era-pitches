from huggingface_hub import HfApi
import datetime
import os

from statcast import update_statcast
from statcast.utils import LOCAL_STATCAST_DATA_LOC


HF_TOKEN = os.environ.get("HF_TOKEN")


def yesterday() -> datetime.date:
    return datetime.datetime.now().date() - datetime.timedelta(days=1)


def upload_to_hf() -> None:
    api = HfApi(token=HF_TOKEN)
    api.upload_file(
        path_or_fileobj=LOCAL_STATCAST_DATA_LOC,
        path_in_repo="data/statcast_era_pitches.parquet",
        repo_id="Jensen-holm/statcast-era-pitches",
        repo_type="dataset",
    )


if __name__ == "__main__":
    update_statcast(date=yesterday())
    upload_to_hf()
