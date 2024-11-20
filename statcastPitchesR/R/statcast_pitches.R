library(arrow)

HF_DB_LOC <- "https://huggingface.co/datasets/Jensen-holm/statcast-era-pitches/resolve/main/data/statcast_era_pitches.parquet"

load <-
  function() {
    return (arrow::open_dataset(HF_DB_LOC))
  }
