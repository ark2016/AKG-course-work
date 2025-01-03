from fastapi import APIRouter, HTTPException
from ..utils.parser.parser import download_images
from ..utils.parser.parser500px import scrape_500px_images
from ..utils.parser.parse_Flickr_API import download_flickr_images
from ..schemas.questions import DownloadImagesRequest, Scrape500pxImagesRequest, \
    DownloadFlickrImagesRequest, CreateDatasetRequest
from ..utils.dataset_utils import images_to_parquet
from ..utils.model_prediction_utils import ModelLoader

router = APIRouter(
    tags=["Questions"]
)


# Маршрут для healthcheck
@router.get("/ping")
def api_ping():
    return "OK"


# Маршрут для скачивания изображений
@router.post("/download_images")
def api_download_images(request: DownloadImagesRequest):
    try:
        print(f"Received request: URL={request.url}, Folder={request.folder}")
        download_images(url=request.url, folder=request.folder)
        return {"message": f"Images downloaded successfully to {request.folder}"}
    except Exception as e:
        print(f'Ошибка при обработке запроса: {e}')
        raise HTTPException(status_code=500, detail=str(e))


# Маршрут для скрапинга изображений с 500px
@router.post("/download_images_with_scrolling")
def api_scrape_500px_images(request: Scrape500pxImagesRequest):
    try:
        print(f"Received request: URL={request.url},  Folder={request.folder}")
        scrape_500px_images(url=request.url, folder=request.folder)
        return {"message": f"Images scraped successfully to {request.folder}"}
    except Exception as e:
        print(f'Ошибка при обработке запроса: {e}')
        raise HTTPException(status_code=500, detail=str(e))


# Маршрут для скачивания изображений с Flickr
@router.post("/download_images_flickr")
def api_download_flickr_images(request: DownloadFlickrImagesRequest):
    try:
        print(f"Received request: Search Text={request.search_text}, Folder={request.folder}, Count={request.count}")
        download_flickr_images(search_text=request.search_text, folder=request.folder, count=request.count)
        return {"message": f"Images downloaded successfully to {request.folder}"}
    except Exception as e:
        print(f'Ошибка при обработке запроса: {e}')
        raise HTTPException(status_code=500, detail=str(e))


# Маршрут для создания датасета
@router.post("/create_dataset")
def create_dataset(request: CreateDatasetRequest):
    """
    Создание датасета из изображений и сохранение в формате .parquet.
    """
    try:
        output_file = images_to_parquet(
            source_dir=request.source_dir,
            output_dir=request.output_dir
        )
        return {"message": "Dataset created successfully", "file_path": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Инициализация загрузчика модели
model_loader = ModelLoader(model_path="models/resnet18_weights.pth")


@router.post("/predict")
def predict(image_path: str):
    """
    Предсказание класса объекта на изображении.
    """
    try:
        result = model_loader.predict(image_path=image_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
