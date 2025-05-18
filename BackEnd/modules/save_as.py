import csv

def save_to_csv(pois, file_path):
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "lat", "long"])
        writer.writeheader()
        writer.writerows(pois)

def load_from_csv(file_path):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]