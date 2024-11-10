from pydantic import BaseModel
from typing import Optional


# Модель запроса для download_images
class DownloadImagesRequest(BaseModel):
    url: str
    folder: Optional[str] = "test"