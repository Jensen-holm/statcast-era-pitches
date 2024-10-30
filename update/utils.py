import os

__all__ = ["LOCAL_STATCAST_DATA_LOC", "HF_DATASET_LOC"]

LOCAL_STATCAST_DATA_LOC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "statcast_era_pitches.parquet",
)

HF_DATASET_LOC = (
    "hf://datasets/Jensen-holm/statcast-era-pitches/data/statcast_era_pitches.parquet"
)
