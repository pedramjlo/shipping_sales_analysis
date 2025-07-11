"""
CREATING A TRANSACTION TABLE OUT OF THE CLEANED DATASET FOR THE MARKET BASKET ANALYSIS 
"""
import pandas as pd
from data_saving.dataSaver import DataSaver



class CreateDataset:
    def __init__(self, df):
        self.df = df
        self.new_dataset = None


    def create_mba_dataset(self):
        # Group by invoice_id to get a list of products per transaction
        transaction_data = self.df.groupby('order_id')['product_name'].apply(list).reset_index()
        unique_products = self.df['product_name'].unique()

        # Create a new DataFrame for one-hot encoding
        one_hot_data = pd.DataFrame(0, index=transaction_data.index, columns=unique_products)
        

        # SAVING THE NEW DATAFRAME
        saver = DataSaver()
        saver.save_cleaned_data(df=one_hot_data, output_dir="dataset/transactions", filename="transactions.csv")


    

