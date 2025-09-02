# main.py

import os
from dotenv import load_dotenv
from fastapi import BackgroundTasks, Body, Depends, FastAPI, Request, HTTPException, status, File
from dependencies import get_urls_content
from logging_config import setup_logging
from rag.service import vector_service
from schemas import TextModelRequest, TextModelResponse
from models import generate_text, models
from scraper import fetch_all
from upload import save_file
from typing import Annotated
from fastapi import UploadFile
from rag.extractor import pdf_text_extractor
from dependencies import get_rag_content

# Load environment variables
load_dotenv()

setup_logging()

app = FastAPI()

@app.post("/generate/text", response_model_exclude_defaults=True)
async def serve_text_to_text_controller(
        request: Request,
        body: TextModelRequest = Body(...),
        urls_content: str = Depends(get_urls_content),
        rag_content: str = Depends(get_rag_content),
    ) -> TextModelResponse:

        prompt = body.prompt + " " + urls_content + rag_content
        output = await generate_text("text", prompt, body.temperature)
        return TextModelResponse(content=output, ip=request.client.host)
        # urls_content = await get_urls_content(body)
        # print(f"web_content: {urls_content}")
        # prompt = body.prompt + " " + urls_content
        # output = await generate_text("text", prompt, body.temperature)
        # return TextModelResponse(content=output, ip=request.client.host)

@app.post("/upload")
async def file_upload_controlelr(
        file: Annotated[UploadFile, File(description="Upload PDFdocuments")],
        bg_text_processor: BackgroundTasks,
    ):
        if file.content_type != "application/pdf":
            raise HTTPException(
                    detail="Only uploading PDF documents are supported",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        try:
            filepath = await save_file(file)
            bg_text_processor.add_task(pdf_text_extractor, filepath)
            bg_text_processor.add_task(vector_service.store_file_content_in_db, filepath.replace("pdf", "text")
                , 512, "knowledgebase", 768)
        except Exception as e:
            raise HTTPException(
                    detail=f"An error occurred while saving file - Error {e}",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return {"filename": file.filename, "message": "File upload successfully"}