from data_wrangling.data_cleaning.dataCleaner import DataCleaner
from data_saving.dataSaver import DataSaver
from database_utils.databaseUtils import Database
from analysis.descriptive_analysis.association_analysis.associationAnalysis import MarketBasketAnalysis
from analysis.descriptive_analysis.clustering_analysis.kMeansClustering import KMeans
from data_extraction.get_population.utilities.getCodes import FipsLookup


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

    



class AssociationAnalysis:
    def __init__(self, df="./dataset/cleaned_data/cleaned_sales_data.csv"):
        self.cls_obj = MarketBasketAnalysis(df=df, mba_on="category")



    def perform_mba(self):
        self.cls_obj.create_mba_dataset()
        frequent_itemsets = self.cls_obj.find_frequency(new_dataset="./dataset/transactions/transactions-category.csv")
        print(self.cls_obj.generate_association_rules(frequent_itemsets))



class ClusteringAnalysis:
    def __init__(self, df="./dataset/cleaned_data/cleaned_sales_data.csv"):
        self.df = df
        self.cls_obj = KMeans(data=self.df)


    def perform_kmean(self):
        self.cls_obj.fit_transform()




class GetFips:
    def __init__(self):
        self.cls_obj = FipsLookup()

    def get(self):
        self.cls_obj.get_fips_codes(
            city_state_list=[
                ("Los Angeles", "California"),
                ("Houston", "Texas"),
                ("Nonexistent City", "Nowhere")
            ]
        )


if __name__ == "__main__":

    """
    Data cleaning, saving, and loading to the database
    """
    pipe = Pipeline()
    pipe.clean_data()
    pipe.save_cleaned_data()
    pipe.load_to_database()


    """
    Market Basket Analysis
    mba = AssociationAnalysis()
    mba.perform_mba()

    cls = ClusteringAnalysis()
    cls.perform_kmean()
    
    """
    

    gf = GetFips()
    gf.get()