import requests

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
        for city, state in city_state_list:
            key = (city.lower(), state.lower())
            fips = self.lookup.get(key)
            if fips:
                results[(city, state)] = {
                    "state_fips": fips[0],
                    "place_fips": fips[1]
                }
            else:
                results[(city, state)] = None  # Not found

        return results


# Usage example
lookup = FipsLookup()
city_state_pairs = [
    ("Los Angeles", "California"),
    ("Houston", "Texas"),
    ("Nonexistent City", "Nowhere")
]

results = lookup.get_fips_codes(city_state_pairs)

for (city, state), fips in results.items():
    if fips:
        print(f"{city}, {state} -> state FIPS: {fips['state_fips']}, place FIPS: {fips['place_fips']}")
    else:
        print(f"{city}, {state} -> NOT FOUND")
