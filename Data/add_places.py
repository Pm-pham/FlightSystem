import csv
from flights.models import Place  # Adjust with your actual app name


def save_airports_to_db(csv_file_path):
    try:
        # Open the CSV file
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            # Create a CSV reader
            csv_reader = csv.DictReader(file)

            # Loop through each row in the CSV file
            for row in csv_reader:
                # Extract the fields from the CSV
                city = row['city']
                airport = row['airport']
                code = row['code']
                country = row['country']

                # Create a Place instance and save it to the database
                # You can use get_or_create() to avoid duplicates
                Place.objects.get_or_create(
                    city=city,
                    airport=airport,
                    code=code,
                    country=country
                )

            print(f"Successfully imported data from {csv_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

