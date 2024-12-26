import torch
from torchvision import models, transforms
from PIL import Image
from fastapi import HTTPException


# Функция для загрузки модели
class ModelLoader:
    def __init__(self, model_path: str):
        try:
            # Загружаем архитектуру модели
            self.model = models.resnet18(pretrained=False)

            # Переопределяем выходной слой в соответствии с сохранённой моделью
            num_classes = 1  # Укажите здесь количество классов вашей задачи
            self.model.fc = torch.nn.Linear(self.model.fc.in_features, num_classes)

            # Загружаем веса
            state_dict = torch.load(model_path, map_location=torch.device('cpu'))
            self.model.load_state_dict(state_dict)
            self.model.eval()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка загрузки модели: {str(e)}")

    def predict(self, image_path: str):
        try:
            # Загрузка изображения
            image = Image.open(image_path).convert("RGB")

            # Преобразования изображения
            transform = transforms.Compose([
                transforms.Resize((224, 224)),  # Изменение размера изображения
                transforms.ToTensor(),  # Преобразование в тензор
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
            input_tensor = transform(image).unsqueeze(0)

            # Выполнение предсказания
            with torch.no_grad():
                output = self.model(input_tensor)
                _, predicted_class = torch.max(output, 1)

            return {"predicted_class": predicted_class.item()}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка предсказания: {str(e)}")
