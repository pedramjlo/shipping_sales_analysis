from data_wrangling.data_cleaning.dataCleaner import DataCleaner



class Pipeline:
    pass



if __name__ == "__main__":
    raw_dataset = "./dataset/raw/sales_data.csv"

    cleaner = DataCleaner(raw_dataset=raw_dataset)
    cleaner.run()