import os
import logging
import csv


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class DataSaver:



    def save_cleaned_data(self, df, output_dir="dataset/cleaned_data", filename="cleaned_sales_data.csv"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, filename)

        try:
            df.to_csv(file_path, index=False)
            logging.info(f"Cleaned data saved to {file_path}")
        except Exception as e:
            logging.error(f"Failed to save cleaned data: {e}")
        
        return file_path
    

    """
    method to save into csv files
    """

    def save_list_of_dicts_to_csv(data, output_dir="output", file_name="data.csv"):
        """
        Save a list of dictionaries to a CSV file.

        Args:
            data (list of dict): Data to save.
            output_dir (str): Directory to save the CSV file.
            filename (str): Name of the CSV file.

        Returns:
            str: Path to the saved CSV file.
        """
        if not data:
            print("No data provided to save.")
            return None

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, file_name)

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Data saved successfully to {file_path}")
            return file_path
        except Exception as e:
            print(f"Failed to save CSV: {e}")
            return None
