from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def get_exif_data(image_path):
    """
    также преобразует GPS теги
    :param image_path:
    :return: словарь с exif данными PIL картинки
    """

    image = Image.open(image_path)
    image.verify()
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data


def get_decimal_from_dms(dms, ref):
    """
    преобразует координаты GPS в десятичный формат
    :param dms:
    :param ref:
    :return:
    """
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0
    decimal = degrees + minutes + seconds
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal


def get_lat_lon(exif_data):
    """
    возвращает широту и долготу из exif_data, если GPS данные есть
    :param exif_data:
    :return:
    """
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = gps_info.get("GPSLatitude")
        gps_latitude_ref = gps_info.get("GPSLatitudeRef")
        gps_longitude = gps_info.get("GPSLongitude")
        gps_longitude_ref = gps_info.get("GPSLongitudeRef")

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = get_decimal_from_dms(gps_latitude, gps_latitude_ref)
            lon = get_decimal_from_dms(gps_longitude, gps_longitude_ref)

    return lat, lon


if __name__ == "__main__":
    image_path = "red_fox_0_500px_images.jpg"
    exif_data = get_exif_data(image_path)
    lat, lon = get_lat_lon(exif_data)
    if lat and lon:
        print(f"Latitude: {lat}, Longitude: {lon}")
    else:
        print("No GPS data found")
