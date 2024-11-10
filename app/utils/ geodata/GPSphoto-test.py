from GPSPhoto import gpsphoto

# Пример использования
image_path = "red_fox_0_500px_images.jpg"
data = gpsphoto.getGPSData(image_path)

if data:
    print(f"Latitude: {data['Latitude']}")
    print(f"Longitude: {data['Longitude']}")
else:
    print("No GPS information found in the image.")