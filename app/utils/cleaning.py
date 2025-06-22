import pandas as pd
from typing import List, Tuple

class CleaningUtils:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def normalize_columns(self, columns: List[str]) -> "CleaningUtils":
        for col in columns:
            if col in self.df.columns and self.df[col].dtype == "object":
                self.df[col] = self.df[col].fillna("").apply(lambda x: x.lower().capitalize())
        return self

    def replace_words(self, replacements: List[Tuple[str, str]], columns: List[str]) -> "CleaningUtils":
        for col in columns:
            if col in self.df.columns and self.df[col].dtype == "object":
                for old, new in replacements:
                    self.df[col] = self.df[col].str.replace(old, new, regex=False)
        return self

    def get_df(self) -> pd.DataFrame:
        return self.df
