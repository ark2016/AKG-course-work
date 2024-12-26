import pandas as pd
import os
import shutil

# Параметры
INPUT_DIRS = [
    "./survey_1_summer_2013",
    "./survey_5_autumn_2013",
    "./survey_10_winter_2013",
    "./survey_17_spring_2014"
]
OUTPUT_DIR = "./combined_dataset"  # Общая папка для всех изображений
ANNOTATION_FILE = "combined_annotations.csv"  # Файл разметки

# Загрузка исходного списка изображений и описаний
image_list = pd.read_csv("image_list.csv")

# Создание выходной директории
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Список для хранения разметки
annotations = []

# Формирование датасета
print("Объединение папок в единый датасет...")

for input_dir in INPUT_DIRS:
    print(f"Обработка папки: {input_dir}")
    for _, row in image_list.iterrows():
        image_name = row['image']  # Название изображения
        file_path = os.path.join(input_dir, image_name)  # Полный путь к изображению
        target_path = os.path.join(OUTPUT_DIR, image_name)  # Новый путь для сохранения

        # Проверка существования файла и его копирование
        if os.path.exists(file_path):
            shutil.copy(file_path, target_path)

            # Добавление записи в аннотацию
            annotations.append({
                "file_path": target_path,
                "label": row['fox_id'],  # Метка: идентификатор лисы
                "season_id": row['season_id'],  # ID сезона (для анализа)
                "survey_id": row['survey_id']  # ID опроса
            })

# Сохранение файла с разметкой
annotations_df = pd.DataFrame(annotations)
annotations_df.to_csv(os.path.join(OUTPUT_DIR, ANNOTATION_FILE), index=False)

print(f"Датасет успешно объединен в {OUTPUT_DIR}")
print(f"Файл разметки сохранен: {os.path.join(OUTPUT_DIR, ANNOTATION_FILE)}")
