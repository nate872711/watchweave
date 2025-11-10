import pandas as pd
from rich import print


class IMDbClient:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_ratings(self):
        """Loads IMDb ratings CSV exported by IMDb."""
        try:
            df = pd.read_csv(self.csv_path)
            return df
        except Exception as e:
            print(f"[red]IMDb CSV error: {e}")
            return pd.DataFrame()
