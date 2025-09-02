# upload.py

import os
import aiofiles
from aiofiles.os import makedirs
from fastapi import UploadFile
from loguru import logger

DEFAULT_CHUNK_SIZE = 1024 * 1024 * 50 # 50 megabytes

async def save_file(file: UploadFile) -> str:
    await makedirs("uploads", exist_ok=True)
    logger.info(f"Saving file: {file.filename}")
    filepath = os.path.join("uploads", file.filename)
    async with aiofiles.open(filepath, "wb") as f:
        while chunk := await file.read(DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
    logger.info(f"File saved: {filepath}")
    return filepath
