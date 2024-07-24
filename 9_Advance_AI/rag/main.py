from fastapi import BackgroundTasks,File,UploadFile,Body,Request, Depends
from fastapi import status,HTTPException 
from fastapi  import FastAPI
from extract import pdf_text_extractor
from typing import Annotated
import uvicorn
import time
import torch
from upload import save_file
from service import vector_service
from schemas import TextModelRequest,TextModelResponse
from vector_search import get_rag_content
from contextlib import asynccontextmanager
from model import m_text



ml_models = {}

@asynccontextmanager
async def liefspan(app : FastAPI):

    device_name = None
    if torch.backends.mps.is_available():
        device_name = "cpu"
    else:
        device_name = "cpu"

    ml_models["text"] = m_text.load_text_model(device_name= device_name)
    yield
    ml_models.clear()



app = FastAPI(lifespan= liefspan)

@app.post("/upload")
async def file_upload_controller(
    file :  Annotated[UploadFile , File(description= "A file read as UploadFile")],
    bg_text_processor : BackgroundTasks,
):
    
    if file.content_type != "application/pdf":
          raise HTTPException(
            detail=f"Only uploading PDF documents are supported",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

    try:
        filepath = await save_file(file)
        bg_text_processor.add_task(pdf_text_extractor, filepath)
        bg_text_processor.add_task(
            vector_service.store_file_content_in_db,
            filepath.replace("pdf","txt"),
            512,
            "knowledgebase",
            768
        )

    except Exception as e:
        raise HTTPException(
            detail=f"An error occurred while saving file - Error: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    return {"filename" : file.filename, "message": "File uploaded successfully"}



@app.post("/get_rag/text", response_model_exclude_defaults=True)
async def serve_getRAG(request: Request,
                       body: TextModelRequest = Body(...)) -> TextModelResponse:
    
    start_time = time.time()
    prompt = body.prompt
    rag_content = await get_rag_content(prompt=prompt)

    print("rag_content : ", rag_content)
    print("########################")
    
    new_prompt = prompt+" "+rag_content
    generated_text = m_text.generate_text(ml_models["text"], new_prompt, body.temperature)


    execution_time =  int(start_time - time.time())
    return TextModelResponse(content = generated_text, execution_time=execution_time, ip =request.client.host)



    
    

if __name__ == "__main__":
    uvicorn.run("main:app",port=8000, reload=True)