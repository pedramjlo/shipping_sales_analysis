import pandas as pd
import logging
import re


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)




class DataCleaner:
    def __init__(self, raw_dataset):
        self.raw_dataset = raw_dataset
        self.df = None


    def read_raw_data(self):
        try:
            self.df = pd.read_csv(self.raw_dataset, encoding="ISO-8859-1", engine='python')
            logging.info("Read the dataset successfully.")
        except FileNotFoundError:
            logging.error("Error: The file was not found.")
        except pd.errors.EmptyDataError:
            logging.error("Error: The file is empty.")
        except pd.errors.ParserError:
            logging.error("Error: The file could not be parsed.")



    """
    Due to columns inconsistent naming, the column names are standardised by adding an underscore and converting to lower cases
    """
    def normalise_columns(self):
        try:
            split_chars = ["-", " "]
            split_pattern = f"[{re.escape(''.join(split_chars))}]"
            self.df.columns = ["_".join(re.split(f"[{re.escape(split_pattern)}]", col.lower())) for col in self.df.columns]

            logging.info(f"Normalised data columns successfully. {self.df.columns}")
        except Exception as e:
            logging.error(f"Error at normalising column names, {e}")


