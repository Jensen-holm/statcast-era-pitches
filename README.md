# statcast-pitches

[![Latest Update](https://github.com/Jensen-holm/statcast-era-pitches/actions/workflows/update_statcast_data.yml/badge.svg)](https://github.com/Jensen-holm/statcast-era-pitches/actions/workflows/update_statcast_data.yml)

[pybaseball](https://github.com/jldbc/pybaseball) is a great tool for downloading baseball data. Even though the library is optimized and scrapes this data in parallel, it can be time consuming. 
 
The point of this repository is to utilize GitHub Actions to scrape new baseball data weekly during the MLB season, and update a parquet file hosted as a huggingface dataset. Reading this data as a huggingface dataset is much faster than scraping the new data each time you re run your code, or just want updated statcast pitch data in general.

The `update.py` script updates each week during the MLB season, updating the [statcast-era-pitches HuggingFace Dataset](https://huggingface.co/datasets/Jensen-holm/statcast-era-pitches) so that you don't have to re scrape this data yourself. 

You can explore the entire dataset in your browser [at this link](https://huggingface.co/datasets/Jensen-holm/statcast-era-pitches/viewer/default/train)

# Installation

```bash
pip install statcast-pitches
```

# Usage

### With statcast_pitches package

**Example 1 w/ polars (suggested)**
```python
import statcast_pitches
import polars as pl

# load all pitches from 2015-present
pitches_lf = statcast_pitches.load()

# filter to get 2024 bat speed data
bat_speed_24_df = (pitches_lf
                    .filter(pl.col("game_date").dt.year() == 2024)
                    .select("bat_speed", "swing_length")
                    .collect())

print(bat_speed_24_df.head(3))
```

output: 
| | bat_speed  | swing_length |
|-|------------|--------------|
| 0 | 73.61710 | 6.92448 |
| 1 | 58.63812 | 7.56904 |
| 2 | 71.71226 | 6.46088 |

**Notes**
- Because `statcast_pitches.load()` uses a LazyFrame, we can load it much faster and even perform operations on it before 'collecting' it into memory. If it were loaded as a DataFrame, this code would execute in ~30-60 seconds, instead it runs between 2-8 seconds. 

**Example 2 Duckdb**
```python
import statcast_pitches

# get bat tracking data from 2024
params = ("2024",)
query_2024_bat_speed = f"""
    SELECT bat_speed, swing_length
    FROM pitches
    WHERE 
        YEAR(game_date) =?
        AND bat_speed IS NOT NULL;
    """

bat_speed_24_df = statcast_pitches.load(
    query=query_2024_bat_speed,
    params=params,
).collect()

print(bat_speed_24_df.head(3))
```

output: 
| | bat_speed  | swing_length |
|-|------------|--------------|
| 0 | 73.61710 | 6.92448 |
| 1 | 58.63812 | 7.56904 |
| 2 | 71.71226 | 6.46088 |

**Notes**:
- If no query is specified, all data from 2015-present will be loaded into a DataFrame.
- The table in your query MUST be called 'pitches', or it will fail.
- Since `load()` returns a LazyFrame, notice that I had to call `pl.DataFrame.collect()` before calling `head()`
- This is slower than the other polars approach, however sometimes using SQL is fun

### With HuggingFace API (not recommended)

***Pandas***

```python
import pandas as pd

df = pd.read_parquet("hf://datasets/Jensen-holm/statcast-era-pitches/data/statcast_era_pitches.parquet")
```

***Polars***

```python
import polars as pl

df = pl.read_parquet('hf://datasets/Jensen-holm/statcast-era-pitches/data/statcast_era_pitches.parquet')
```

***Duckdb***

```sql
SELECT *
FROM 'hf://datasets/Jensen-holm/statcast-era-pitches/data/statcast_era_pitches.parquet';
```

***HuggingFace Dataset***

```python
from datasets import load_dataset

ds = load_dataset("Jensen-holm/statcast-era-pitches")
```

***Tidyverse***
```r
library(tidyverse)

statcast_pitches <- read_parquet(
    "https://huggingface.co/datasets/Jensen-holm/statcast-era-pitches/resolve/main/data/statcast_era_pitches.parquet"
)
```

see the [dataset](https://huggingface.co/datasets/Jensen-holm/statcast-era-pitches) on HugingFace itself for more details. 

## Eager Benchmarking

![dataset_load_times](dataset_load_times.png)

| Eager Load Time (s) | API |
|---------------|-----|
| 1421.103 | pybaseball |
| 26.899 | polars |
| 33.093 | pandas |
| 68.692 | duckdb |

# ⚠️ Data-Quality Warning ⚠️

MLB states that real time `pitch_type` classification is automated and subject to change as data gets reviewed. This is currently not taken into account as the huggingface dataset gets updated. `pitch_type` is the only column that is affected by this.

# Contributing

Feel free to submit issues and PR's if you have a contribution you would like to make.
