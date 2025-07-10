import pandas as pd
import logging

class DataCleaner:
    def __init__(self, raw_dataset):
        self.raw_dataset = raw_dataset
        self.df = None


    def read_raw_data(self):
        try:
            self.df = pd.read_csv(self.raw_data, encoding="ISO-8859-1", engine='python')
            logging.info("Read the dataset successfully.")
        except FileNotFoundError:
            logging.error("Error: The file was not found.")
        except pd.errors.EmptyDataError:
            logging.error("Error: The file is empty.")
        except pd.errors.ParserError:
            logging.error("Error: The file could not be parsed.")