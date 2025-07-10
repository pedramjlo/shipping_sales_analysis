import os
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class DataSaver:
    def save_clean_data(self, df, output_dir="dataset/cleaned_data", filename="cleaned_sales_data.csv"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, filename)

        try:
            df.to_csv(file_path, index=False)
            logging.info(f"Cleaned data saved to {file_path}")
        except Exception as e:
            logging.error(f"Failed to save cleaned data: {e}")
        
        return file_path