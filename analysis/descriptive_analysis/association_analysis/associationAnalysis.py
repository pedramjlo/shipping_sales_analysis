"""
CREATING A TRANSACTION TABLE OUT OF THE CLEANED DATASET FOR THE MARKET BASKET ANALYSIS 
"""
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from data_saving.dataSaver import DataSaver
import logging



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

saver = DataSaver()


class MarketBasketAnalysis:
    def __init__(self, df):
        self.df = df


    def create_mba_dataset(self):
        self.df = pd.read_csv(self.df)
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


            # Convert the one-hot DataFrame to boolean type
            one_hot_data = one_hot_data.astype(bool)

            # SAVING THE NEW DATAFRAME
            saver.save_cleaned_data(df=one_hot_data, output_dir="dataset/transactions", filename="transactions.csv")

            
            logging.info("Created a dataset for market basket analysis successfully")

        except Exception as e:
            logging.error(f"Failed to create a dataset for market basket analysis {e}")


        


    """
    The Apriori algorithm is used to find frequent itemsets. 
    You can set a minimum support threshold to specify the minimum frequency for an itemset to be considered "frequent."
    """
    def find_frequency(self, new_dataset):
        new_dataset = pd.read_csv(new_dataset)
        try:
            # Check if the dataset is in the correct format
            logging.info(f"Dataset Shape: {new_dataset.shape}")
            logging.info(f"Dataset Columns: {new_dataset.columns}")
            logging.info(f"Dataset First 5 rows:\n{new_dataset.head()}")

            # Ensure the dataset contains boolean values
            new_dataset = new_dataset.astype(bool)

            # Apply the Apriori algorithm to find frequent itemsets
            frequent_itemsets = apriori(new_dataset, min_support=0.001, use_colnames=True)
            
            # Check if frequent_itemsets is empty
            if frequent_itemsets.empty:
                logging.warning("No frequent itemsets found!")
                return None
            

            # saving the frequency table in a new file
            saver.save_cleaned_data(df=frequent_itemsets, output_dir="dataset/transactions/results", filename="frequency.csv")
            
            logging.info("Calculated the frequency successfully")
            return frequent_itemsets

        except Exception as e:
            logging.error(f"Failed to calculate the frequency: {e}")
            return None

