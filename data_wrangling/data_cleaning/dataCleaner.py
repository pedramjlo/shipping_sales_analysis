import pandas as pd
import numpy as np
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



    """
    Checking the states columns to verify the values of states column
    """
    def check_states_column(self):
        us_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
        try:
            for state in self.df["state"]:
                if not state in us_states:
                    self.df["state"] = np.nan
                    logging.info(f"State {state} wasn't in the list. replace with NaN")
            logging.info("States checked successfully")
        except Exception as e:
            logging.error(f"error in checking states names, {e}")


    def 



