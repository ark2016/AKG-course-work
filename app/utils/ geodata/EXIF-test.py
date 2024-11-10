import exifread


def get_geotagging(filename):
    # Открываем файл изображения
    with open(filename, 'rb') as f:
        tags = exifread.process_file(f)

    # Ищем теги GPSLatitude и GPSLongitude
    latitude = tags.get('GPSLatitude')
    latitude_ref = tags.get('GPSLatitudeRef')
    longitude = tags.get('GPSLongitude')
    longitude_ref = tags.get('GPSLongitudeRef')

    if latitude and longitude:
        # Преобразуем координаты в десятичный формат
        lat = convert_to_degrees(latitude)
        if latitude_ref.values != 'N':
            lat = -lat

        lon = convert_to_degrees(longitude)
        if longitude_ref.values != 'E':
            lon = -lon

        return lat, lon
    else:
        return None, None


def convert_to_degrees(value):
    # Преобразуем координаты из формата DMS (градусы, минуты, секунды) в десятичный формат
    d = float(value.values[0])
    m = float(value.values[1])
    s = float(value.values[2])
    return d + (m / 60.0) + (s / 3600.0)


# Пример использования
filename = 'red_fox_0_500px_images.jpg'
latitude, longitude = get_geotagging(filename)

if latitude is not None and longitude is not None:
    print(f"Широта: {latitude}, Долгота: {longitude}")
else:
    print("Координаты не найдены.")