from data_wrangling.data_cleaning.dataCleaner import DataCleaner



class Pipeline:
    pass



if __name__ == "__main__":
    raw_dataset = "./dataset/raw/sales_data.csv"

    cleaner = DataCleaner(raw_dataset=raw_dataset)
    cleaner.read_raw_data()
    cleaner.normalise_columns()
    cleaner.check_states_column()
    cleaner.check_shipping_modes()
    cleaner.convert_date_columns()
    cleaner.check_country_column()
    cleaner.check_customer_name_id_integrity()
    cleaner.check_customer_segment_column()