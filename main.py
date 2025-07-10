from data_wrangling.data_cleaning.dataCleaner import DataCleaner
from data_saving.dataSaver import DataSaver
from database_utils.databaseUtils import Database


class Pipeline:
    def __init__(self, raw_data="./dataset/raw/sales_data.csv"):
        self.raw_data = raw_data
        self.cleaned_data = None

    def clean_data(self):
        cleaner = DataCleaner(raw_dataset=self.raw_data)
        self.cleaned_data = cleaner.run()

    def save_cleaned_data(self):
        saver = DataSaver()
        saver.save_cleaned_data(df=self.cleaned_data)


    def load_to_database(self):
        db = Database()
        db.create_database() 
        db.load_to_db()



if __name__ == "__main__":
    pipe = Pipeline()
    pipe.clean_data()
    pipe.save_cleaned_data()
    pipe.load_to_database()
    