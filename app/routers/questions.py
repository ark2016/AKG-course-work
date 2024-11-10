from fastapi import APIRouter, HTTPException
from ..utils.parser.parser import download_images  # Импортируем функцию
from ..utils.parser.parser500px import scrape_500px_images  # Импортируем функцию
from ..schemas.questions import DownloadImagesRequest, Scrape500pxImagesRequest  # Импортируем схемы

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
@router.post("/scrape_500px_images")
def api_scrape_500px_images(request: Scrape500pxImagesRequest):
    try:
        print(f"Received request: URL={request.url},  Folder={request.folder}")
        scrape_500px_images(url=request.url, folder=request.folder)
        return {"message": f"Images scraped successfully to {request.folder}"}
    except Exception as e:
        print(f'Ошибка при обработке запроса: {e}')
        raise HTTPException(status_code=500, detail=str(e))
