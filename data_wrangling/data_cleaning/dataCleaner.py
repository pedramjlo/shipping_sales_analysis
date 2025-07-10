import pandas as pd
from logging.logger import Logger


log = Logger().get_logger()


class DataCleaner:
    def __init__(self, raw_dataset):
        self.raw_dataset = raw_dataset
        self.df = None


    def read_raw_data(self):
        try:
            self.df = pd.read_csv(self.raw_data, encoding="ISO-8859-1", engine='python')
            log.info("Read the dataset successfully.")
        except FileNotFoundError:
            log.error("Error: The file was not found.")
        except pd.errors.EmptyDataError:
            log.error("Error: The file is empty.")
        except pd.errors.ParserError:
            log.error("Error: The file could not be parsed.")