# statcast-era-pitches

[pybaseball](https://github.com/jldbc/pybaseball) is a great tool for downloading baseball data. Even though the library is optimized and scrapes this data in parallel, it can be time consuming. 
 
The point of autoball is to utilize GitHub Actions to scrape new baseball data each day during the MLB season, and update a parquet file hosted as a huggingface dataset. Reading this data as a huggingface dataset would be much faster than scraping the new data each time you re run a jupyter notebook, or just want new data in general.

The `main.py` script updates each day during the MLB season, updating the `data/updated_statcast_pitches.parquet` so that you don't have to re scrape this data yourself. 

---
# The Data

The data itself includes every pitch thrown in MLB from 2015 - Present. There is a [data dictionary](https://baseballsavant.mlb.com/csv-docs) for most of the columns included in this dataset on baseball savant. 

