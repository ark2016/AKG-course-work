import os
import pandas as pd
from PIL import Image
from io import BytesIO


def images_to_parquet(source_dir: str, output_dir: str, output_filename: str = "dataset.parquet"):
    """
    Функция для преобразования изображений из директории в формат parquet.
    """
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

    # Список для хранения данных
    data = []

    # Читаем все файлы в директории
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)

        try:
            # Читаем изображение и конвертируем его в bytes
            with Image.open(file_path) as img:
                img_bytes = BytesIO()
                img.save(img_bytes, format=img.format or "JPEG")  # Сохраняем изображение в bytes
                data.append({
                    "file_name": file_name,
                    "image_data": img_bytes.getvalue()  # Массив байтов
                })
        except Exception as e:
            print(f"Ошибка при обработке файла {file_name}: {e}")

    if not data:
        raise ValueError("No valid images found in the source directory.")

    # Создаем DataFrame
    df = pd.DataFrame(data)

    # Создаем выходную директорию, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Сохраняем DataFrame в формате parquet
    output_path = os.path.join(output_dir, output_filename)
    df.to_parquet(output_path, engine="pyarrow")
    print(f"Датасет сохранен в {output_path}")
    return output_path
