from fastapi import APIRouter, HTTPException
from ..utils.parser.parser import download_images  # Импортируем функцию
from ..utils.parser.parser500px import scrape_500px_images  # Импортируем функцию
from ..utils.parser.parse_Flickr_API import download_flickr_images  # Импортируем функцию
from ..schemas.questions import DownloadImagesRequest, Scrape500pxImagesRequest, \
    DownloadFlickrImagesRequest  # Импортируем схемы

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