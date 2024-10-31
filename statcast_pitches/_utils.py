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
