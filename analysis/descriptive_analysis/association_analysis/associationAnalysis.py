"""
CREATING A TRANSACTION TABLE OUT OF THE CLEANED DATASET FOR THE MARKET BASKET ANALYSIS 
"""
import pandas as pd
from data_saving.dataSaver import DataSaver
import logging



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)




class CreateDataset:
    def __init__(self, df):
        self.df = df
        self.new_dataset = None


    def create_mba_dataset(self):
        try:
            # Group by invoice_id to get a list of products per transaction
            transaction_data = self.df.groupby('order_id')['product_name'].apply(list).reset_index()
            unique_products = self.df['product_name'].unique()

            # Create a new DataFrame for one-hot encoding
            one_hot_data = pd.DataFrame(0, index=transaction_data.index, columns=unique_products)

            # Loop through each transaction and mark the products bought
            for idx, transaction in transaction_data.iterrows():
                for product in transaction['product_name']:
                    one_hot_data.at[idx, product] = 1
            
            logging.info("Created a dataset for market basket analysis successfully")

        except Exception as e:
            logging.error(f"Failed to create a dataset for market basket analysis {e}")


        # SAVING THE NEW DATAFRAME
        saver = DataSaver()
        saver.save_cleaned_data(df=one_hot_data, output_dir="dataset/transactions", filename="transactions.csv")


    

