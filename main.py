from data_wrangling.data_cleaning.dataCleaner import DataCleaner
from data_saving.dataSaver import DataSaver
from database_utils.databaseUtils import Database
from analysis.descriptive_analysis.association_analysis.associationAnalysis import CreateDataset


class Pipeline:
    def __init__(self, raw_data="./dataset/raw/sales_data.csv"):
        self.raw_data = raw_data
        self.cleaned_data = None


    """
    cleaning the data
    """
    def clean_data(self):
        cleaner = DataCleaner(raw_dataset=self.raw_data)
        self.cleaned_data = cleaner.run()


    """
    saving the cleaned data into a new csv file
    """
    def save_cleaned_data(self):
        saver = DataSaver()
        saver.save_cleaned_data(df=self.cleaned_data)

    """
    loading the cleaned data to the PostgreSQL database 
    """
    def load_to_database(self):
        db = Database()
        db.create_database() 
        db.load_to_db()

    """
    creating a dataset for market basket analysis
    """
    def create_mba_data(self):
        cd = CreateDataset(df=self.cleaned_data)
        cd.create_mba_dataset()



if __name__ == "__main__":
    pipe = Pipeline()
    pipe.clean_data()
    pipe.save_cleaned_data()
    pipe.load_to_database()
    
    
    pipe.create_mba_data()

    
    