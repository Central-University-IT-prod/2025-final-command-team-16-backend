# utils/files.py
import os
import shutil
import uuid

from fastapi import HTTPException, UploadFile

from src.core.config import settings

os.makedirs(settings.upload_dir, exist_ok=True)


async def save_uploaded_file(file: UploadFile) -> str:
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(settings.upload_dir, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при сохранении файла: {e!s}"
        )

    return unique_filename


def get_file_url(filename: str) -> str:
    return f"/static/{filename}"
