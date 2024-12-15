import csv
from flights.models import Place


def load_airport_data_from_csv(file_path):
    # Mở và đọc dữ liệu từ CSV
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Lấy các giá trị từ mỗi dòng trong CSV
            city = row['city']
            airport = row['airport']
            code = row['code']
            country = row['country']

            # Kiểm tra xem địa điểm đã tồn tại trong cơ sở dữ liệu chưa
            if not Place.objects.filter(code=code).exists():
                # Nếu chưa tồn tại, tạo một đối tượng Place mới và lưu vào cơ sở dữ liệu
                place = Place(
                    city=city,
                    airport=airport,
                    code=code,
                    country=country
                )

                place.save()

    print(f'Data from {file_path} loaded successfully!')