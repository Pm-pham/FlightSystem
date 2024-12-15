import csv
from datetime import datetime, timedelta
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from flights.models import Place, Week, Flight  # Update based on your app and model names

def load_flights(csv_file_path):
    """
    Load flights data from a CSV file into the database.
    """
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            # Cache for objects to reduce DB hits
            weekday_cache = {}
            place_cache = {}

            flights_batch = []
            batch_size = 500  # Adjust based on your system's performance

            for i, row in enumerate(reader, start=1):
                try:
                    # Get or create origin and destination places
                    origin_code = row['origin'].upper()
                    destination_code = row['destination'].upper()

                    if origin_code not in place_cache:
                        place_cache[origin_code], _ = Place.objects.get_or_create(code=origin_code)
                    if destination_code not in place_cache:
                        place_cache[destination_code], _ = Place.objects.get_or_create(code=destination_code)

                    origin = place_cache[origin_code]
                    destination = place_cache[destination_code]

                    # Get or create weekday
                    weekday_number = int(row['depart_weekday'])
                    if weekday_number not in weekday_cache:
                        weekday, _ = Week.objects.get_or_create(
                            number=weekday_number,
                            defaults={
                                'name': [
                                    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                                    'Friday', 'Saturday', 'Sunday'
                                ][weekday_number]
                            }
                        )
                        weekday_cache[weekday_number] = weekday
                    else:
                        weekday = weekday_cache[weekday_number]

                    # Parse duration
                    hours, minutes, seconds = map(int, row['duration'].split(':'))
                    duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)

                    # Prepare flight object
                    flight = Flight(
                        origin=origin,
                        destination=destination,
                        depart_time=datetime.strptime(row['depart_time'], "%H:%M:%S").time(),
                        duration=duration,
                        arrival_time=datetime.strptime(row['arrival_time'], "%H:%M:%S").time(),
                        plane=row['flight_no'],
                        airline=row['airline'],
                        economy_fare=float(row['economy_fare']) if row['economy_fare'] else None,
                        business_fare=float(row['business_fare']) if row['business_fare'] else None,
                        first_fare=float(row['first_fare']) if row['first_fare'] else None,
                    )

                    flights_batch.append((flight, weekday))

                    # Insert in batches
                    if len(flights_batch) >= batch_size:
                        save_batch(flights_batch)
                        flights_batch.clear()
                        print(f"Processed {i} rows...")

                except Exception as row_error:
                    print(f"Error processing row {i}: {row_error}")

            # Save remaining flights
            if flights_batch:
                save_batch(flights_batch)

            print(f"Successfully loaded {i} flights from {csv_file_path}")

    except Exception as e:
        print(f"Error loading flights: {e}")

def save_batch(flights_batch):
    """
    Save a batch of flights and associate them with weekdays.
    """
    try:
        flights = [flight for flight, _ in flights_batch]
        Flight.objects.bulk_create(flights)

        # Handle many-to-many relations
        for flight, weekday in flights_batch:
            flight.depart_day.add(weekday)

        print(f"Saved batch of {len(flights)} flights.")
    except Exception as e:
        print(f"Error saving batch: {e}")

if __name__ == "__main__":
    csv_file = r"D:\PythonProject\Project_Python\Data\international_flights.csv"
    load_flights(csv_file)
