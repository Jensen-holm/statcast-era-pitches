from typing import Optional
import os

__all__ = ["HF_DATASET_LOC", "INSTALL_DB_REQS_QUERY", "REGISTER_QUERY", "read_sql"]

HF_DATASET_LOC = (
    "hf://datasets/Jensen-holm/statcast-era-pitches/data/statcast_era_pitches.parquet"
)


INSTALL_DB_REQS_QUERY = """
    INSTALL httpfs;
    LOAD httpfs;
"""


REGISTER_QUERY = f"""
    CREATE VIEW pitches AS 
    SELECT * FROM parquet_scan('{HF_DATASET_LOC}');
"""


def _is_sql(fp: str) -> bool:
    ext = os.path.splitext(fp)[-1]
    return True if os.path.exists(fp) and ext == ".sql" else False


def read_sql(fp: str) -> Optional[str]:
    """
    Reads the contents of a SQL file if the input is a valid .sql file, None otherwise

    Arguments
    --------
    fp : str
        string or a filepath to a .sql file

    Returns
    -------
    file contents of the file located at `fp` if it is a valid .sql file, else None
    """
    if not _is_sql(fp):
        return None

    with open(fp, "r") as f:
        sql = f.read()
    return sql
