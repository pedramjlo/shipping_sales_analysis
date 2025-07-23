import requests
from data_saving.dataSaver import DataSaver



"""
Since the U.S. Census Bureau API required the FIPS code of states and cities
to fetch relevant data;
    - the FIPS codes of states are retrieved 
    - Saved in a new directory and CSV file 
"""

class FipsLookup:
    def __init__(self, year="2010", dataset="dec/sf1"):
        self.base_url = f"https://api.census.gov/data/{year}/{dataset}"
        self.lookup = None

    def load_data(self):
        params = {
            "get": "NAME",
            "for": "place:*",
            "in": "state:*"
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Build dictionary: {(city_lower, state_lower): (state_fips, place_fips)}
        self.lookup = {}
        for row in data[1:]:  # skip header
            full_name, state_fips, place_fips = row

            # Parse city and state from full_name: "Los Angeles city, California"
            if ", " in full_name:
                city_part, state_part = full_name.split(", ")
                # Remove suffixes like ' city', ' town', etc.
                city_name = city_part.rsplit(" ", 1)[0].lower()
                state_name = state_part.lower()

                self.lookup[(city_name, state_name)] = (state_fips, place_fips)

                
    def get_fips_codes(self, city_state_list):
        if self.lookup is None:
            self.load_data()

        results = {}
        rows = []

        for city, state in city_state_list:
            key = (city.lower(), state.lower())
            fips = self.lookup.get(key)

            if fips:
                results[(city, state)] = {
                    "state_fips": fips[0],
                    "place_fips": fips[1]
                }

                # Add to list for saving
                rows.append({
                    "city": city,
                    "state": state,
                    "state_fips": fips[0],
                    "place_fips": fips[1]
                })
            else:
                results[(city, state)] = None  # Not found

        # Save to CSV
        ds = DataSaver()
        ds.save_list_of_dicts_to_csv(data=rows, output_dir="state_codes", file_name="fips_codes.csv")

        return results
