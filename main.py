import pandas as pd
import sqlite3
import time
from app.infraestructure import ColombiaSenadoScraper
from app.utils.cleaning import CleaningUtils

class Main:

    @staticmethod
    def save_df_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str, if_exists: str = "replace"):
        """
        Guarda un DataFrame en una base de datos SQLite.
        """
        try:
            with sqlite3.connect(db_path) as conn:
                df.to_sql(name=table_name, con=conn, if_exists=if_exists, index=False)
            print(f"Datos guardados en {db_path}, tabla: {table_name}")
        except Exception as e:
            print(f"Error al guardar en SQLite: {e}")

    @staticmethod
    def run():
        start = time.time()

        scraper = ColombiaSenadoScraper()
        laws = scraper.scrape_colombia_laws()

        if laws is not None:
            cleaning = CleaningUtils(laws)
            replacements = [("Estado actual:", ""), ('“', ""), ('"', ""), ('”', "")]

            df = (
                cleaning.replace_words(replacements=replacements, columns=["status", "title"])
                        .normalize_columns(columns=laws.columns.to_list())
                        .get_df()
            )

            Main.save_df_to_sqlite(df, "laws_colombia.db", "laws")

        end = time.time()
        elapsed = end - start
        print(f"Tiempo total de ejecución: {elapsed:.2f} segundos")

if __name__ == "__main__":
    Main.run()
