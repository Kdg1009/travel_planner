import csv
import os

def save_as(poi_list: list, filename: str, format: str = 'csv'):
    path = os.path.join("BackEnd","routes", "temp", filename)
    
    if format == 'csv':
        if not poi_list:
            raise ValueError("POI list is empty, nothing to save.")

        # Ensure the "temp" directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Get CSV fieldnames from the first item keys
        fieldnames = poi_list[0].keys()

        with open(path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for poi in poi_list:
                writer.writerow(poi)