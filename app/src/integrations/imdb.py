import logging
import pandas as pd

log = logging.getLogger("imdb")

class IMDbClient:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_ratings(self):
        """Load IMDb ratings CSV (exported from IMDb)."""
        try:
            df = pd.read_csv(self.csv_path)
            return df
        except Exception as e:
            log.exception(f"IMDb CSV load error: {e}")
            return pd.DataFrame()
