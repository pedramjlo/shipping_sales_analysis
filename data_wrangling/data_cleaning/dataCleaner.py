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
            logging.info("States checked successfully. All values are correct.")
        except Exception as e:
            logging.error(f"error in checking states names, {e}")


    """
    Checking whether the only available shipping modes are listed
    """
    def check_shipping_modes(self):
        shipping_methods = ["Second Class", "Standard Class", "First Class", "Same Day"]
        try:
            for mode in self.df["ship_mode"]:
                if not mode in shipping_methods:
                    self.df["ship_mode"] = np.nan
                    logging.info(f"Shipping modes {mode} wasn't in the list. replace with NaN")
            logging.info("Shipping modes checked successfully. All values are correct.")
        except Exception as e:
            logging.error(f"error in checking shipping modes, {e}")


    
    """
    Converting the Americanised date format (dd/mm/yyyy) to ISO (yyyy-mm-dd)
    """
    def convert_date_columns(self, date_columns=["order_date", "ship_date"]):
        try:
            for date_column in date_columns:
                # Convert date to datetime format (with error handling)
                self.df[date_column] = pd.to_datetime(self.df[date_column], format='%d/%m/%Y', errors='coerce')

                # Check if conversion was successful
                if self.df[date_column].isnull().any():
                    logging.warning(f"Some entries in {date_column} could not be converted and are now NaT.")

                # Optionally, standardize the format to 'YYYY-MM-DD'
                self.df[date_column] = self.df[date_column].dt.strftime('%Y-%m-%d')

                logging.info(f"{date_column} values successfully converted to yyyy-mm-dd format.")

        except Exception as e:
            logging.error(f"Error in converting date formats: {e}")


    """
    Checking if all country columns contain United States as the value
    """
    def check_country_column(self):
        try:
            if not (self.df["country"] == "United States").all():
                # set non "United States" values to NaN
                self.df["country"] = self.df["country"].apply(lambda x: x if x == "United States" else np.nan)
                logging.info(f"Non-United States values converted to NaN")
            else:
                logging.info("All Country values are correct. No need for conversion.")
        except Exception as e:
            logging.error(f"Error in converting country values: {e}")


    """
    Checking for the integrity of customers' names and their ID
    """
    def check_customer_name_id_integrity(self):
        try:
            inconsistent_rows = self.df[self.df.duplicated(subset=['customer_id'], keep=False) & 
                (self.df['customer_name'] != self.df.groupby('customer_id')['customer_name'].transform('first'))]
            if not inconsistent_rows.empty:
                logging.warning(f"Inconsistent Customer id-name found: {inconsistent_rows}")
            logging.info("No incosistent id-name columns were found.")
        except Exception as e:
            logging.error(f"Inconsistency in customer name-id columns: {e}")


    """
    Checking if Segment column only contains the valid values
    """
    def check_customer_segment_column(self):
        segments = ["Consumer", "Corporate", "Home Office"]
        try:
            # Check if all values are valid segments
            if not (self.df["segment"].isin(segments)).all():
                # Set invalid values to NaN
                self.df["segment"] = self.df["segment"].apply(lambda x: np.nan if x not in segments else x)
                logging.info(f"Invalid values converted to NaN")
            else:
                logging.info("All segment values are correct. No need for conversion.")
        except Exception as e:
            logging.error(f"Error in converting segment values: {e}")



    """
    are all region column values valid?
    """
    def check_region_column(self):
        regions = ["South", "West", "Central", "East"]
        try:
            # Check if all values are valid segments
            if not (self.df["region"].isin(regions)).all():
                # Set invalid values to NaN
                self.df["region"] = self.df["region"].apply(lambda x: np.nan if x not in regions else x)
                logging.info(f"Invalid values converted to NaN")
            else:
                logging.info("All region values are correct. No need for conversion.")
        except Exception as e:
            logging.error(f"Error in converting region values: {e}")

            
    """
    The is an issue with the postal code column where the values contain a period at the end.
    This function strips them.
    """
    def strip_postal_code_period(self):
        try:
            # Convert postal code to int if it's a float (to remove '.0'), else leave as is
            self.df['postal_code'] = self.df['postal_code'].apply(
                lambda x: int(x) if isinstance(x, float) and not pd.isna(x) else x
            )
            logging.info("Stripped the period from the postal codes")
        except Exception as e:
            logging.error(f"Error in stripping the periods from the postal code values: {e}")


    """
    converting 2 date columns, order date & ship date from pandas objects to date types
    """
    def convert_date_types(self, date_columns=["order_date", "ship_date"]):
        try:
            for date_column in date_columns:
                self.df[date_column] = pd.to_datetime(self.df[date_column], errors='coerce')
                logging.info(f"Successfully converted {date_column} to datetime.")
        except Exception as e:
            logging.warning(f"Failed to convert {date_column} to datetime type: {e}")

    """
    dropping duplicate rows
    """
    def drop_duplicate_rows(self):
        total_rows = self.df.shape[0]
        duplicate_rows = self.df.duplicated().sum()
        
        try:
            if duplicate_rows == 0:
                logging.info("No duplicate rows were found")
            else:
                self.df = self.df.drop_duplicates()
                removed_rows = total_rows - self.df.shape[0]
                logging.info(f"{removed_rows} rows were removed")
        except Exception as e:
            logging.error(f"Failed to drop duplicate rows, {e}")


    """
    central function to run all the cleaner pipeline methods
    """
    def run(self):
        self.read_raw_data()
        self.normalise_columns()
        self.check_states_column()
        self.check_shipping_modes()
        self.convert_date_columns()
        self.check_country_column()
        self.check_customer_name_id_integrity()
        self.check_customer_segment_column()
        self.check_region_column()
        self.strip_postal_code_period()
        self.convert_date_types()
        self.drop_duplicate_rows()
        return self.df